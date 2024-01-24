"""
github
unique user
unique business
chat id
"""

from django.db import models


class Chat(models.Model):
    key = models.CharField(max_length=100, primary_key=True)
    

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    bot_key = models.CharField(max_length=100, primary_key=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)


class Instruction(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    instruction = models.TextField()
    index = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        """ Validate that the index is unique for the business """
        bussiness_instructions = Instruction.objects.filter(business=self.business)
        instructions_indexes = list(map(
            lambda instruction: instruction.index, bussiness_instructions
        ))
        if self.index in instructions_indexes:
            raise Exception('Index already exists')
        
        super(Instruction, self).save(*args, **kwargs)


class User(models.model):
    id = models.AutoField(primary_key=True)
    key = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)