from django.contrib import admin
from . import models


@admin.register(models.TelegramToken)
class TelegramTokenAdmin(admin.ModelAdmin):
    list_display = ('business', 'token',)
    search_fields = ('business', 'token',)
    
    
@admin.register(models.WelcomeMessage)
class WelcomeMessageAdmin(admin.ModelAdmin):
    list_display = ('origin', 'business', 'message')
    search_fields = ('origin', 'business', 'message')