from django.contrib import admin
from . import models

admin.site.site_header = "ChatGPT Chatbot Service"
admin.site.site_title = "ChatGPT Chatbot Service"
admin.site.site_url = '/'
admin.site.index_title = "Admin"


@admin.register(models.Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'assistent_key', 'whatsapp_number')
    list_filter = ('is_active',)
    search_fields = ('name', 'assistent_key')
    
    
@admin.register(models.Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('index', 'instruction', 'business')
    list_filter = ('business',)
    ordering = ('business', 'index')
    

@admin.register(models.Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'key', 'name', 'chat_key', 'origin')
    list_filter = ('business', 'origin')
    search_fields = ('key', 'name', 'chat_key')
    

@admin.register(models.DataFile)
class DataFileAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'business', 'file_link')
    list_filter = ('business',)
    search_fields = ('name', 'file_link')