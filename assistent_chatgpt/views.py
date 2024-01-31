import os
import json
from dotenv import load_dotenv
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .chatbot import ChatBot
from business_data import models as business_models
from . import models as assistent_models

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
        user_key = data['user']['key']
        user_origin = data['user']['origin']
        user_name = data['user']['name']
        
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
        
        # Get business
        business = assistent_models.Business.objects.get(name=business_name)
        
        # Validate if user already exists
        user_found = assistent_models.User.objects.filter(
            key=user_key
        )
        if user_found:
            # Get chat id
            chat = user_found[0].chat
        else:
            # Validate origin
            origin = assistent_models.Origin.objects.filter(
                name=user_origin
            )
            if origin:
                origin = origin[0]
            else:
                return JsonResponse({
                    "status": "error",
                    "message": "The user origin is not valid for this business",
                    "data": {}
                }, status=400)
            
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
            
            # Initialize chatbot
            chatbot = ChatBot(instructions, products)
        
            # Create chat
            chat = chatbot.create_chat()
            
            # Save user
            assistent_models.User.objects.create(
                business=business,
                key=user_key,
                name=user_name,
                chat=chat,
                origin=origin,
            )
        
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