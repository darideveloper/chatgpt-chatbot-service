from django.db import models
    

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    

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


class Origin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)


class User(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    name = models.CharField(max_length=100, blank=True, null=True)
    chat = models.CharField(max_length=100)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        """ Validate that the key is unique for the business and origin """
        bussiness_origin_users = User.objects.filter(
            business=self.business, origin=self.origin
        )
        users_keys = list(map(
            lambda user: user.key, bussiness_origin_users
        ))
        if self.key in users_keys:
            raise Exception('Key already exists')
        
        super(User, self).save(*args, **kwargs)
    
    
class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    
    def save(self, *args, **kwargs):
        """ Validate that the origin is unique for the business """
        bussiness_bots = Bot.objects.filter(business=self.business)
        bots_origins = list(map(
            lambda bot: bot.origin, bussiness_bots
        ))
        if self.origin in bots_origins:
            raise Exception('Origin already exists')
        
        super(Bot, self).save(*args, **kwargs)
