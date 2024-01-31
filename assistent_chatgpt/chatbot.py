import os
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv

# Load env variables
load_dotenv()
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")


class ChatBot():
    
    def __init__(self, instructions: list, products: list):
        """ Start basic chatbot
        
        Args:
            instructions (list): assistent instructions
            products (list): products in csv format
        """
        
        print("Creating chatbot...")
        
        # Generic final instruction
        instructions.append("A continuación se muestra en formato csv, "
                            "la información de los productos: ")
        
        # Convert instructions and products to string
        instructions = "\n".join(instructions)
        products = "\n".join(products)
    
        # Connext openai
        self.client = OpenAI(api_key=API_KEY_OPENAI)
       
        # Create assistant
        self.assistant = self.client.beta.assistants.create(
            name="Asistente de Refaccionaria X",
            instructions=f"{instructions}\n\n{products}",
            tools=[{"type": "code_interpreter"}],
            model="gpt-4-1106-preview"
        )
    
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
    
    def get_response(self, thread_id: str) -> str:
        """ Wait in loop for a chatgpt response

        Args:
            thread_id (str): chatgpot chat id

        Returns:
            str: chatgpt response
        """
    
        # Start running chat in bg
        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=self.assistant.id,
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
    
        
    