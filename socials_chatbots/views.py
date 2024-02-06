import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from threading import Thread
from socials_chatbots.libs.telegram import send_response
from socials_chatbots import models as socials_chatbots_models
from assistent_chatgpt import models as assistent_chatgpt_models


@method_decorator(csrf_exempt, name='dispatch')
class TelegramChat(View):
    def post(self, request, business_name):
        
        print(f"Webhook received for {business_name}")
        
        # Get message
        json_data = json.loads(request.body)
        message = json_data.get("message", "")

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

        # Get message part
        message_text = message["text"]
        message_chat_id = message["chat"]["id"]
        username = message["from"]["username"]

        # Send message in background
        message_thread = Thread(
            target=send_response,
            args=(
                message_text,
                business_name,
                username,
                message_chat_id,
                "telegram",
                token,
            )
        )
        message_thread.start()

        # Confirm message received to telegram
        return JsonResponse({
            "status": "success",
            "message": "Message received",
            "data": {}
        }, status=200)
