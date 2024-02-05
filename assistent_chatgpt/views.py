import os
import json
from dotenv import load_dotenv
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .chatbot import ChatBot
from business_data.models import business_tables
from . import models as assistent_models

# Load env variables
load_dotenv()
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")


@method_decorator(csrf_exempt, name='dispatch')
class Chat(View):
    def post(self, request):
        
        # Instance chatbot
        chatbot = ChatBot(
            assistent_models.Business,
            assistent_models.Instruction
        )
        
        # Get user message from json
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        message = data.get('message', '')
        business_name = data.get('business', '')
        user_key = data.get('user', {}).get('key', '')
        user_origin = data.get('user', {}).get('origin', '')
        user_name = data.get('user', {}).get('name', '')
        
        # Validate required data
        required_fields = [message, business_name, user_key, user_origin]
        for field in required_fields:
            if not field:
                return JsonResponse({
                    "status": "error",
                    "message": "The message, business, "
                               "user key and user origin are required",
                    "data": {}
                }, status=400)
        
        # Validate if the business name
        if business_name not in business_tables:
            return JsonResponse({
                "status": "error",
                "message": "The business name is not valid",
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
            chat_key = user_found[0].chat_key
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
                    "message": "The user origin is not valid",
                    "data": {}
                }, status=400)
                
            # Create chat
            chat_key = chatbot.create_chat()
            
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
            assistent_key = chatbot.create_assistent_business(business_name)
            
        # Send message and wait for response
        chatbot.send_message(chat_key, message)
        try:
            response = chatbot.get_response(chat_key, assistent_key)
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