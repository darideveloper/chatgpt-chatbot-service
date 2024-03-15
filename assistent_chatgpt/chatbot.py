import json
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv
from . import models as assistent_models
import urllib.parse

# Load env variables
load_dotenv()


class ChatBot():
    
    def __init__(self, Business, Instruction, api_key: str):
        """ Start basic chatbot
        
        Args:
            Business (class): business model
            Instruction (class): instruction model
            api_key (str): openai api key
        """
        
        print("Creating chatbot...")
    
        # Connext openai
        self.client = OpenAI(api_key=api_key)
        
        # Save models
        self.Business = Business
        self.Instruction = Instruction
        
    def __get_business_instructions__(self, business_name: str) -> tuple:
        """ Get business instructions

        Args:
            business_name (str): business name

        Returns:
            tuple:
                (obj) business instance
                (list) instructions texts
        """
        
        business = self.Business.objects.get(name=business_name)
        
        # Get instructions
        instructions_objs = self.Instruction.objects.filter(
            business=business,
        ).order_by('index')
        instructions_text = [
            instruction.instruction for instruction in instructions_objs
        ]
        
        return business, instructions_text
    
    def create_assistent(self, business_name: str, first_instruction: str) -> str:
        """ Create assistant and return assistant id
        
        Args:
            business_name (str): business name
            first_instruction (str): first instruction
        
        Returns:
            str: chatgpt assistant id
        """
                
        # Create assistant with initial instructions
        assistant = self.client.beta.assistants.create(
            name=f"Asistente {business_name}",
            instructions=first_instruction,
            tools=[{"type": "code_interpreter"}],
            model="gpt-3.5-turbo-0125",
            # file_ids=files_ids,
        )
        
        return assistant.id
    
    def create_assistent_business(self, business_name: str) -> str:
        """ Create an asistent for a specific business (with instructions and products)

        Args:
            business_name (str): business name

        Returns:
            str: chatgpt assistant id
        """
        
        print(f"Creating assistent for business {business_name}...")
    
        business, instructions_objs = self.__get_business_instructions__(business_name)
        if not instructions_objs:
            return ""
        first_instruction = business.prompt
        
        # Create assistent
        assistent_key = self.create_assistent(business_name, first_instruction)
        
        # Update bot id in business
        business.assistent_key = assistent_key
        business.save()
        
        return assistent_key
    
    def load_products(self, user_key: str, user_origin: str,
                      user_name: str, business_name: str,
                      products_objs: list):
        """ Send products to chatgpt as messages

        Args:
            products (list): products data in csv format
        """
        
        chat_key = self.create_user_chat(
            user_key=user_key,
            user_origin=user_origin,
            user_name=user_name,
            business_name=business_name,
        )
        
        # Get products data
        products = ""
        if products_objs:
            # Save products
            columns = products_objs[0].get_cols()
            products = [product.get_str() for product in products_objs]
            products.insert(0, columns)
    
        # Split products in chunks
        products_in_chunk = 20
        products = [
            products[i:i + products_in_chunk]
            for i in range(0, len(products), products_in_chunk)
        ]
            
        # Send products
        for chunk in products:
            products_text = "\n".join(chunk)
            self.send_message(chat_key, products_text)
        
    def create_chat(self, business_name: str) -> str:
        """ Credate and return chat id
        
        Args:
            business_name (str): business name
            
        Returns:
            str: chat gpt chat id
        """
        
        print("Creating chat...")
        
        # Create new chat
        thread = self.client.beta.threads.create()
        
        # Send remaining instructions as messages
        _, instructions = self.__get_business_instructions__(business_name)
        for instruction in instructions:
            self.send_message(thread.id, instruction)
            
        return thread.id
        
    def send_message(self, chat_key: str, message: str):
        """ Send new message in specific chat

        Args:
            chat_key (str): chatgpt chat id
            message (str): message sent from user
            role (str): user or assistant (default: user)
        """
        
        print(f"Sending message: {message} to chat {chat_key}")
        
        # Add messages to the chat
        self.client.beta.threads.messages.create(
            thread_id=chat_key,
            role="user",
            content=message
        )
    
    def get_response(self, chat_key: str, assistant_key: str,
                     set_typing: object, bot_token: str, user_key: str) -> str:
        """ Wait in loop for a chatgpt response

        Args:
            chat_key (str): chatgpot chat id
            assistant_key (str): chatgpt assistant id
            set_typing (object): set typing function
            bot_token (str): telegram bot token
            user_key (str): user key in the chat platform

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
            
            # Get response from chatgpt
            run = self.client.beta.threads.runs.retrieve(
                thread_id=chat_key,
                run_id=run.id
            )
            if run.completed_at:
                break
            
            # Activate typing animation
            set_typing(
                bot_token,
                user_key,
            )
            
            sleep(2)
                    
        # Get response from chatgpt
        messages = self.client.beta.threads.messages.list(
            thread_id=chat_key
        )
        response = messages.data[0].content[0].text.value
        return response
    
    def create_user_chat(self, user_key: str, user_origin: str, user_name: str,
                         business_name: str) -> str:
        """ Create a new user in system and his chat
        
        Args:
            user_key (str): user key in the chat platform
            user_origin (str): user chat platform (like telegram, whatsapp, etc.)
            user_name (str): user username in the chat platform
            business (object): business instance
            business_name (str): business name
        
        Returns:
            str: chatgpt chat id
        """
        
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
            chat_key = self.create_chat(
                business_name=business_name,
            )
            
            # Save user in database
            assistent_models.User.objects.create(
                business=business,
                key=user_key,
                name=user_name,
                chat_key=chat_key,
                origin=origin
            )
            
        return chat_key
    
    def workflow(self, message: str, business_name: str, user_key: str,
                 user_origin: str, user_name: str, set_typing: object,
                 bot_token: str) -> str:
        """ Chatbot workflow: validate user info, business name, create assistent,
            create chat, send message and get response from chatgpt
        
        Args:
            message (str): user message
            business_name (str): business name
            user_key (str): user key in the chat platform
            user_origin (str): user chat platform (like telegram, whatsapp, etc.)
            user_name (str): user username in the chat platform
            set_typing (object): set typing function
            bot_token (str): telegram bot token
        """
            
        # Validate required data
        required_fields = [message, business_name, user_key, user_origin]
        for field in required_fields:
            if not field:
                raise ValueError("The message, business, user key and "
                                 "user origin are required")
            
        # Get business
        business = assistent_models.Business.objects.get(name=business_name)
        
        chat_key = self.create_user_chat(
            user_key=user_key,
            user_origin=user_origin,
            user_name=user_name,
            business_name=business_name,
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
            response = self.get_response(
                chat_key,
                assistent_key,
                set_typing,
                bot_token,
                user_key,
            )
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