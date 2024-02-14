import os
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv

# Load env variables
load_dotenv()
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")


class ChatBot():
    
    def __init__(self, Business, Instruction):
        """ Start basic chatbot
        
        Args:
            Business (class): business model
            Instruction (class): instruction model
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
        
        # Create assistant
        assistant = self.client.beta.assistants.create(
            name="Asistente de Refaccionaria X",
            instructions=f"{self.instructions}\n\n{self.products}",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
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