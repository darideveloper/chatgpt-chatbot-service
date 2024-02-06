from django.urls import path
from socials_chatbots.views import TelegramChat

urlpatterns = [
    path('telegram/<business_name>', TelegramChat.as_view(), name='chat'),
]
