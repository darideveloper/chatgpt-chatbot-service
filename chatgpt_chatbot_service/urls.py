from django.contrib import admin
from django.urls import path, include
from socials_chatbots.urls import urlpatterns as socials_chatbots_urls
from assistent_chatgpt.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('webhook/', include(socials_chatbots_urls)),
]
