from django.contrib import admin
from django.urls import path, include
from assistent_chatgpt.urls import urlpatterns as assistent_chatgpt_urls
from socials_chatbots.urls import urlpatterns as socials_chatbots_urls
from assistent_chatgpt.views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(assistent_chatgpt_urls)),
    path('webhook/', include(socials_chatbots_urls)),
]
