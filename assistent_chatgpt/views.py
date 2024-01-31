import os
import json
from dotenv import load_dotenv
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .chatbot import ChatBot
from business_data import models as business_models
from . import models as chat_models

# Load env variables
load_dotenv()
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")


@method_decorator(csrf_exempt, name='dispatch')
class Chat(View):
    def post(self, request):
        
        # Get user message from json
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        message = data['message']
        business_name = data['business']
        
        # Tables relation
        business_tables = {
            "refaccionaria x": business_models.RefaccionariaX,
            "refaccionaria y": business_models.RefaccionariaY,
        }
        
        # Validate if the business name
        if business_name not in business_tables:
            return JsonResponse({
                "status": "error",
                "message": "The business name is not ready for process files",
                "data": {}
            }, status=400)
        
        # Get instructions
        business = chat_models.Business.objects.get(name=business_name)
        instructions_objs = chat_models.Instruction.objects.filter(
            business=business,
        ).order_by('index')
        instructions = [instruction.instruction for instruction in instructions_objs]
        
        # Get products
        products_objs = business_tables[business_name].objects.all()
        columns = products_objs[0].get_cols()
        products = [product.get_str() for product in products_objs]
        products.insert(0, columns)
        
        # Initialize chatbot
        chatbot = ChatBot(instructions, products)
        
        # Create chat
        chat = chatbot.create_chat()
        
        # Send message and wait for response
        chatbot.send_message(chat, message)
        try:
            response = chatbot.get_response(chat)
        except Exception:
            return JsonResponse({
                "status": "error",
                "message": "Chatgpt is not responding",
                "data": {}
            }, status=500)
            
        # Return response
        return JsonResponse({
            "status": "success",
            "message": "Chatgpt is responding",
            "data": {
                "response": response,
            }
        }, status=200)