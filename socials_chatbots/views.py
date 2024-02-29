import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from threading import Thread
from socials_chatbots.libs import telegram
from socials_chatbots import models as socials_chatbots_models
from assistent_chatgpt import models as assistent_chatgpt_models
from business_data.models import business_tables
from assistent_chatgpt.chatbot import ChatBot


@method_decorator(csrf_exempt, name='dispatch')
class TelegramChat(View):
    def post(self, request, business_name):
        
        # return JsonResponse({
        #     "status": "success",
        #     "message": "Message received",
        #     "data": {}
        # }, status=200)

        print(f"Webhook received for {business_name}")
        
        # Get message
        json_data = json.loads(request.body)
        message = json_data.get("message", "")
        print(f"Message received: {message}")

        # Return default confirmation message
        if not message:
            return JsonResponse({
                "status": "success",
                "message": "No message received",
                "data": {}
            }, status=200)

        # Get telegram token
        business = assistent_chatgpt_models.Business.objects.get(name=business_name)
        token = socials_chatbots_models.TelegramToken.objects.get(business=business)
        
        # Get unique categories from products model
        categories_keyboard = {}
        business_products = business_tables[business_name]
        if business_products:
            categories = business_products.objects.all().values("category").distinct()
            categories = [category["category"] for category in categories]
            
            # Create custom keyboard with categories
            buttons = []
            for category in categories:
                buttons.append([{"text": f"{category}"}])
            
            categories_keyboard = {
                'keyboard': buttons,
                'resize_keyboard': True
            }
            
        # Get message part
        message_text = message.get("text", "hola")
        message_chat_id = message["chat"]["id"]
        username = message["from"].get("username", "")
        if not username:
            first_name = message["from"].get("first_name", "")
            last_name = message["from"].get("last_name", "")
            username = f"{first_name} {last_name}"
        
        if message_text in ["/start", "/iniciar"]:
            # Get welcome message
            origin_telegram = assistent_chatgpt_models.Origin.objects.get(
                name="telegram"
            )
            welcome_message = socials_chatbots_models.WelcomeMessage.objects.filter(
                origin=origin_telegram,
                business=business
            )
            if welcome_message:
                welcome_message = welcome_message[0].message
            else:
                welcome_message = "Bienvenido a nuestro chatbot"
            
            # Send welcome message to user
            telegram.send_message(
                bot_token=token,
                user_key=message_chat_id,
                message=welcome_message,
                keyboard=categories_keyboard,
            )
            
            # Confirm start message received to telegram
            return JsonResponse({
                "status": "success",
                "message": "Start message received",
                "data": {}
            }, status=200)
            
        # Set typing action
        telegram.set_typing(
            bot_token=token,
            user_key=message_chat_id
        )
                        
        # Send message in background
        message_thread = Thread(
            target=telegram.send_message_chatgpt,
            args=(
                message_text,
                business_name,
                username,
                message_chat_id,
                "telegram",
                token,
                ChatBot,
                assistent_chatgpt_models,
                categories_keyboard,
            )
        )
        message_thread.start()

        # Confirm message received to telegram
        return JsonResponse({
            "status": "success",
            "message": "Message received",
            "data": {}
        }, status=200)
