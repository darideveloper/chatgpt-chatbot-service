from django.db import models
from .chatbot import ChatBot
from django.contrib.auth.models import User as AuthUser
from django.utils import timezone

    
class Business(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    assistent_key = models.CharField(max_length=100, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=100, blank=True, null=True)
    openai_apikey = models.CharField(max_length=100, default="")
    prompt = models.TextField(default="")
    auth_user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    end_message_1 = models.TextField(default="")
    end_message_2 = models.TextField(default="")
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Businesses"
        verbose_name = "Business"
        

class Instruction(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    instruction = models.CharField(max_length=15000)
    
    def __str__(self):
        return f"{self.id}. {self.instruction[:20]}..."
        
    def save(self, *args, **kwargs):
        """ Update assistent each time an instruction is saved """
        
        # Create new assistent
        chatbot = ChatBot(Business, Instruction, self.business.openai_apikey)
        assistent_id = chatbot.create_assistent_business(self.business.name)
        
        # Save chatbot id
        self.business.assistent_key = assistent_id
        self.business.save()
        
        super(Instruction, self).save(*args, **kwargs)
        

class Origin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name


class User(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True, null=True)
    chat_key = models.CharField(max_length=100)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    last_update = models.DateTimeField()
    end_messages_sent = models.BooleanField(default=False)
    
    class Meta:
        """ Validate that the key is unique for the business and origin """
        unique_together = ('business', 'key', 'origin')
        
    def __str__(self):
        return f"{self.key} ({self.origin})"