from django.db import models
from assistent_chatgpt.models import Business


class TelegramToken(models.Model):
    token = models.CharField(max_length=200)
    business = models.OneToOneField(Business, on_delete=models.CASCADE)

    def __str__(self):
        return self.token