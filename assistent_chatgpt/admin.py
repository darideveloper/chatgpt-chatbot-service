import os
from dotenv import load_dotenv
from . import models
from django.contrib import admin

# env variabled
load_dotenv()
MAX_INSTRUCTIONS = int(os.getenv("MAX_INSTRUCTIONS", 10))


admin.site.site_header = "ChatGPT Chatbot Service"
admin.site.site_title = "ChatGPT Chatbot Service"
admin.site.site_url = '/'
admin.site.index_title = "Admin"


@admin.register(models.Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'assistent_key')
    list_filter = ('is_active',)
    search_fields = ('name', 'assistent_key', 'prompt')
    
    
@admin.register(models.Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'instruction', 'business')
    list_filter = ('business',)
    ordering = ('id', 'business')
    
    # Custom error when save model
    def save_model(self, request, obj, form, change):
        
        # Count instructions
        instructions_num = models.Instruction.objects.filter(
            business=obj.business
        ).count()
        
        # Show error message to user in admin
        if instructions_num > MAX_INSTRUCTIONS:
            self.message_user(
                request,
                f"Exceeded the maximum number of instructions"
                f" for the business '{obj.business.name}'",
                level='ERROR'
            )
            return
        else:
            super(InstructionAdmin, self).save_model(request, obj, form, change)
        

@admin.register(models.Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'key', 'name', 'chat_key', 'origin')
    list_filter = ('business', 'origin')
    search_fields = ('key', 'name', 'chat_key')