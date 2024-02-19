import os
import json
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv
from . import models as assistent_models
import urllib.parse
import requests

# Load env variables
load_dotenv()
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")


class ChatBot():
    
    def __init__(self, Business, Instruction, remote_files=[]):
        """ Start basic chatbot
        
        Args:
            Business (class): business model
            Instruction (class): instruction model
            remote_files (object): data files instances
        """
        
        print("Creating chatbot...")
        
        # Bot data
        self.products = ""
        self.instructions = ""
    
        # Connext openai
        self.client = OpenAI(api_key=API_KEY_OPENAI)
        
        # Save models
        self.Business = Business
        self.Instruction = Instruction
        self.remote_files = remote_files
    
    def set_instructions(self, instructions: list):
        """ Set new instructions
        
        Args:
            instructions (list): new instructions
        """
        
        print("Setting new instructions...")
        
        # Convert instructions and products to string
        self.instructions = "\n".join(instructions)
        
    def set_products(self, products: list):
        """ Set new products
        
        Args:
            products (list): new products
        """
        
        print("Setting new products...")
        
        # Generic final instruction
        products.insert("A continuación se muestra"
                        "la información de los productos: ", 0)
        
        self.products = "\n".join(products)
    
    def create_assistent(self) -> str:
        """ Create assistant and return assistant id
        
        Returns:
            str: chatgpt assistant id
        """
        
        # Load files with chatgpt
        files_ids = []
        for remote_file in self.remote_files:
            
            # Download file with requests
            res = requests.get(remote_file.file_link)
            
            # Upload file to chatgpt
            file = self.client.files.create(
                file=res.content,
                purpose='assistants'
            )
            files_ids.append(file.id)
        
        # Create assistant
        assistant = self.client.beta.assistants.create(
            name="Asistente de Refaccionaria X",
            instructions=f"{self.instructions}\n\n{self.products}",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview",
            file_ids=files_ids,
        )
        return assistant.id
    
    def create_assistent_business(self, business_name: str) -> str:
        """ Create an asistent for a specific business (with instructions and products)

        Args:
            business_name (str): business name

        Returns:
            str: chatgpt assistant id
        """
        
        # Import business tables
        from business_data.models import business_tables
        
        print(f"Creating assistent for business {business_name}...")
    
        business = self.Business.objects.get(name=business_name)
        
        # Get instructions
        instructions_objs = self.Instruction.objects.filter(
            business=business,
        ).order_by('index')
        instructions = [instruction.instruction for instruction in instructions_objs]
        
        # Set instructions
        self.set_instructions(instructions)
        
        # Get products
        try:
            products_objs = business_tables[business_name].objects.all()
        except Exception:
            products_objs = []
            
        if products_objs:
            # Save products
            columns = products_objs[0].get_cols()
            products = [product.get_str() for product in products_objs]
            products.insert(0, columns)
            self.set_products(products)
        
        # Create assistent
        assistent_key = self.create_assistent()
        
        # Update bot id in business
        business.assistent_key = assistent_key
        business.save()
        
        return assistent_key
        
    def create_chat(self) -> str:
        """ Credate and return chat id
        
        Returns:
            str: chat gpt chat id
        """
        
        print("Creating chat...")
        
        # Create new chat
        thread = self.client.beta.threads.create()
        return thread.id
        
    def send_message(self, chat_key: str, message: str):
        """ Send new message in specific chat

        Args:
            chat_key (str): chatgpt chat id
            message (str): message sent from user
        """
        
        print(f"Sending message: {message} to chat {chat_key}")
        
        # Add messages to the chat
        self.client.beta.threads.messages.create(
            thread_id=chat_key,
            role="user",
            content=message
        )
    
    def get_response(self, chat_key: str, assistant_key: str) -> str:
        """ Wait in loop for a chatgpt response

        Args:
            chat_key (str): chatgpot chat id

        Returns:
            str: chatgpt response
        """
    
        # Start running chat in bg
        run = self.client.beta.threads.runs.create(
            thread_id=chat_key,
            assistant_id=assistant_key,
            timeout=30
        )
    
        # Wait until chatgot is complete
        while True:
            
            print(f"Getting response from chat {chat_key}...")
            
            run = self.client.beta.threads.runs.retrieve(
                thread_id=chat_key,
                run_id=run.id
            )
            if run.completed_at:
                break
            sleep(2)
                    
        # Get response from chatgpt
        messages = self.client.beta.threads.messages.list(
            thread_id=chat_key
        )
        response = messages.data[0].content[0].text.value
        return response
    
    def workflow(self, message: str, business_name: str, user_key: str,
                 user_origin: str, user_name: str) -> str:
        """ Chatbot workflow: validate user info, business name, create assistent,
        create chat, send message and get response from chatgpt """
        
        from business_data.models import business_tables
    
        # Validate required data
        required_fields = [message, business_name, user_key, user_origin]
        for field in required_fields:
            if not field:
                raise ValueError("The message, business, user key and "
                                 "user origin are required")
                
        # Validate if the business name
        if business_name not in business_tables:
            raise ValueError("The business name is not valid")
            
        # Get business
        business = assistent_models.Business.objects.get(name=business_name)
        
        # Validate if user already exists
        user_found = assistent_models.User.objects.filter(
            key=user_key,
            business=business,
        )
        if user_found:
            # Get chat id
            chat_key = user_found[0].chat_key
        else:
            # Validate origin
            origin = assistent_models.Origin.objects.filter(
                name=user_origin
            )
            if origin:
                origin = origin[0]
            else:
                raise ValueError("The user origin is not valid")
                
            # Create chat
            chat_key = self.create_chat()
            
            # Save user in database
            assistent_models.User.objects.create(
                business=business,
                key=user_key,
                name=user_name,
                chat_key=chat_key,
                origin=origin
            )
            
        # Create assistent if not exists
        assistent_key = business.assistent_key
        if not assistent_key:
            assistent_key = self.create_assistent_business(business_name)
        
        # Send message and wait for response
        error_mesage = "Chatgpt is not responding"
        try:
            self.send_message(chat_key, message)
        except Exception:
            raise ValueError(error_mesage)
        
        try:
            response = self.get_response(chat_key, assistent_key)
            print(f"chatgpt response: {response}")
        except Exception:
            raise ValueError(error_mesage)
        
        # Detect end of the chat with json response
        if "json" in response:
            
            # Format response
            response = response.replace("json", "").replace("```", "")
            response = json.loads(response)
            summary = ""
            for response_key, response_value in response.items():
                summary += f"{response_key}: {response_value}\n"
                
            # Get whatsapp number
            whatsapp_number = business.whatsapp_number
            base_message = f"Muchas gracias por usar nuestro asistente " \
                           f"virtual de {business_name}. "
                           
            if whatsapp_number:
                
                # Create whatsapp link
                summary = urllib.parse.quote(summary)
                whatsapp_link = "https://api.whatsapp.com/" \
                    f"send?phone={whatsapp_number}&text={summary}"
                
                # Go to sales message
                message = f"{base_message} Continua con la compra en el " \
                    f"siguiente enlace: {whatsapp_link}"
                    
                response = message
            else:
                response = f"{base_message} Contacta a ventas o visita " \
                    "nuestra sucursal más cercana"
            
        # Return response
        return response