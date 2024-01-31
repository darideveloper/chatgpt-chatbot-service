import os
from time import sleep
from openai import OpenAI
from dotenv import load_dotenv

# Load env variables
load_dotenv()
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")


class ChatBot():
    
    def __init__(self, instructions: list, products: list):
        """ Start basic chatbot """
        
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
    
    def create_chat(self):
        # Create new chat
        thread = self.client.beta.threads.create()
        return thread
        
    def send_message(self, thread, message):
        # Add messages to the chat
        self.client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )
    
    def get_response(self, thread):
    
        # Start running chat in bg
        run = self.client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=self.assistant.id,
            # instructions="Please address the user as Jane Doe."
            #              "The user has a premium account."
            timeout=30
        )
    
        # Wait until chatgot is complete
        while True:
            run = self.client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if run.completed_at:
                break
            sleep(2)
        
        # Get response from chatgpt
        messages = self.client.beta.threads.messages.list(
            thread_id=thread.id
        )
        response = messages.data[0].content[0].text.value
        return response
    
        
    