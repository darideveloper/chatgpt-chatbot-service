from django.db import models
    

class Business(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
    

class Instruction(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    instruction = models.TextField()
    index = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.index}. {self.instruction[:20]}..."
    
    class Meta:
        """ Validate that the index is unique for the business """
        unique_together = ('business', 'index')


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
    chat = models.CharField(max_length=100)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    
    class Meta:
        """ Validate that the key is unique for the business and origin """
        unique_together = ('business', 'key', 'origin')
        
    def __str__(self):
        return f"{self.key} ({self.origin})"
    
    
class Bot(models.Model):
    id = models.AutoField(primary_key=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    origin = models.ForeignKey(Origin, on_delete=models.CASCADE)
    
    class Meta:
        """ Validate that the origin is unique for the business """
        unique_together = ('business', 'origin')

    def __str__(self):
        return f"{self.key} ({self.origin})"