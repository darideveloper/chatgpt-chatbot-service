import os
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv
from . import models as assistent_models
from business_data.models import business_tables

# Load env variables
load_dotenv()
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")


class ChatBot():
    
    def __init__(self):
        """ Start basic chatbot
        
        Args:
            instructions (list): assistent instructions
            products (list): products in csv format
        """
        
        print("Creating chatbot...")
        
        # Bot data
        self.products = ""
        self.instructions = ""
    
        # Connext openai
        self.client = OpenAI(api_key=API_KEY_OPENAI)
    
    def set_instructions(self, instructions: list):
        """ Set new instructions
        
        Args:
            instructions (list): new instructions
        """
        
        print("Setting new instructions...")
        
        # Generic final instruction
        instructions.append("A continuación se muestra"
                            "la información de los productos: ")
        
        # Convert instructions and products to string
        self.instructions = "\n".join(instructions)
        
    def set_products(self, products: list):
        """ Set new products
        
        Args:
            products (list): new products
        """
        
        print("Setting new products...")
        
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
        
        print(f"Creating assistent for business {business_name}...")
    
        business = assistent_models.Business.objects.get(name=business_name)
        
        # Get instructions
        instructions_objs = assistent_models.Instruction.objects.filter(
            business=business,
        ).order_by('index')
        instructions = [instruction.instruction for instruction in instructions_objs]
        
        # Get products
        products_objs = business_tables[business_name].objects.all()
        columns = products_objs[0].get_cols()
        products = [product.get_str() for product in products_objs]
        products.insert(0, columns)
        
        # Set instructions and products
        self.set_instructions(instructions)
        self.set_products(products)
        
        # Create assistent
        assistent_id = self.create_assistent()
        
        # Update bot id in business
        business.bot_key = assistent_id
        business.save()
        
        return assistent_id
        
    def create_chat(self) -> str:
        """ Credate and return chat id
        
        Returns:
            str: chat gpt chat id
        """
        
        print("Creating chat...")
        
        # Create new chat
        thread = self.client.beta.threads.create()
        return thread.id
        
    def send_message(self, thread_id: str, message: str):
        """ Send new message in specific chat

        Args:
            thread_id (str): chatgpt chat id
            message (str): message sent from user
        """
        
        print(f"Sending message: {message} to chat {thread_id}")
        
        # Add messages to the chat
        self.client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
    
    def get_response(self, thread_id: str, assistant_id: str) -> str:
        """ Wait in loop for a chatgpt response

        Args:
            thread_id (str): chatgpot chat id

        Returns:
            str: chatgpt response
        """
    
        # Start running chat in bg
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            timeout=30
        )
    
        # Wait until chatgot is complete
        while True:
            
            print(f"Getting response from chat {thread_id}...")
            
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )
            if run.completed_at:
                break
            sleep(2)
                    
        # Get response from chatgpt
        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id
        )
        response = messages.data[0].content[0].text.value
        return response
    
    
if __name__ == "__main__":
    # Test chatbot
    instructions = [
        "Hola, soy un asistente virtual",
        "Estoy aquí para ayudarte",
        "Por favor, dime tu nombre"
    ]
    products = [
        "ID,Nombre,Precio",
        "1,Producto 1,100",
        "2,Producto 2,200",
        "3,Producto 3,300"
    ]
    chatbot = ChatBot(instructions, products)
    assistent_id = chatbot.create_assistent()
    chat_id = chatbot.create_chat()
    
    while True:
        message = input("message: ")
        chatbot.send_message(chat_id, message)
        print(chatbot.get_response(chat_id, assistent_id))