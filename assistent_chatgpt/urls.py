from django.urls import path
from assistent_chatgpt.views import Chat

urlpatterns = [
    path('chat/', Chat.as_view(), name='chat'),
]
