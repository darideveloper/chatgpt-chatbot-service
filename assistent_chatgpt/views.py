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
import urllib.parse

# Load env variables
load_dotenv()
API_KEY_OPENAI = os.getenv("API_KEY_OPENAI")


def home(request):
    return JsonResponse({
        "status": "success",
        "message": "Welcome to assistent chatgpt",
        "data": {}
    }, status=200)
    

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
        try:
            chatbot.send_message(chat_key, message)
        except Exception:
            return JsonResponse({
                "status": "success",
                "message": "Chatgpt already loading",
                "data": {
                    "response": "Estamos procesando su mensaje anterior, "
                                "espere un momento"
                                "\nLe agradeceremos enviar un mensaje a la vez.",
                }
            }, status=200)
        
        try:
            response = chatbot.get_response(chat_key, assistent_key)
            print(f"chatgpt response: {response}")
        except Exception:
            return JsonResponse({
                "status": "error",
                "message": "Chatgpt is not responding",
                "data": {}
            }, status=500)
            
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
        return JsonResponse({
            "status": "success",
            "message": "Chatgpt is responding",
            "data": {
                "response": response,
            }
        }, status=200)