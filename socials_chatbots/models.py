import os
from dotenv import load_dotenv
from django.db import models
from assistent_chatgpt.models import Business
import requests

load_dotenv()
HOST = os.getenv("HOST")


class TelegramToken(models.Model):
    token = models.CharField(max_length=200)
    business = models.OneToOneField(Business, on_delete=models.CASCADE)

    def __str__(self):
        return self.token
    
    def save(self, *args, **kwargs):
        
        # Generate webhook
        dynamic_webhook = f"{HOST}/webhook/telegram/{self.business.name}"
        url = f"https://api.telegram.org/bot{self.token}" \
            f"/setWebhook?url={dynamic_webhook}"
        
        # Send request to save webhook
        res = requests.get(url)
        if res.status_code != 200:
            raise Exception("Error setting webhook")
            
        super(TelegramToken, self).save(*args, **kwargs)