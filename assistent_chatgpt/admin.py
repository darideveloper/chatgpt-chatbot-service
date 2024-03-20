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


class InstrucctionUserListFilter(admin.SimpleListFilter):

    # Label
    title = "Bot"
    parameter_name = "bot"
    
    def lookups(self, request, model_admin) -> list:
        """ Generate options list
        
        Returns:
            list: list of tuples with options
        """
        
        auth_user = request.user
                
        # Get all business from instruction
        instructions = model_admin.model.objects.all()
        businesses = list(map(lambda instruction: instruction.business, instructions))
        if auth_user.is_superuser:
            businesses_user = businesses
        else:
            businesses_user = list(filter(
                lambda business: business.auth_user == auth_user, businesses
            ))
        businesses_unique = list(set(businesses_user))
        options = []
        for business in businesses_unique:
            options.append((business.name, business.name))
        
        return options
    
    def queryset(self, request, queryset):
        """ Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        """
        
        data = queryset.filter(
            business__name=self.value()
        )
        
        return data
    

@admin.register(models.Business)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'assistent_key', 'auth_user')
    list_filter = ('is_active', 'auth_user')
    search_fields = ('name', 'assistent_key', 'prompt', 'auth_user')
    
    
@admin.register(models.Instruction)
class InstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'instruction', 'business')
    list_filter = (InstrucctionUserListFilter,)
    ordering = ('id', 'business')
    
    # Custom error when save model
    def save_model(self, request, obj, form, change):
        
        # Count instructions
        instructions_num = models.Instruction.objects.filter(
            business=obj.business
        ).count()
        
        # Show error message to user in admin
        if instructions_num >= MAX_INSTRUCTIONS:
            self.message_user(
                request,
                f"Exceeded the maximum number of instructions"
                f" for the business '{obj.business.name}'",
                level='ERROR'
            )
            return
        else:
            super(InstructionAdmin, self).save_model(request, obj, form, change)
            
    def get_queryset(self, request):
            
        # Get admin type
        user_auth = request.user
        if not user_auth.is_superuser:
            
            # Filter instructions by user
            return models.Instruction.objects.filter(business__auth_user=user_auth)
            
        # Render all instructions
        return models.Instruction.objects.all()
    
    
@admin.register(models.Origin)
class OriginAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    

@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'business', 'key', 'name', 'chat_key',
                    'origin', 'last_update', 'end_messages_sent')
    list_filter = ('business', 'origin', 'last_update')
    search_fields = ('key', 'name', 'chat_key')