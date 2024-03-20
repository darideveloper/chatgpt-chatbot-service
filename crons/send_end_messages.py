""" Send custom end message per business to users that
have not been updated in specific time"""

# Add parent folder to path
import os
import sys
import django
from dotenv import load_dotenv
parent_folder = os.path.dirname(os.path.dirname(__file__))
sys.path.append(parent_folder)

# Env variables
load_dotenv()
SEND_END_MESSAGE_MINUTES = int(os.getenv("SEND_END_MESSAGE_MINUTES"))

# Setup django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatgpt_chatbot_service.settings')
django.setup()

# Django imports
from assistent_chatgpt import models as assistent_models
from socials_chatbots import models as socials_models
from django.utils import timezone
from socials_chatbots.libs.telegram import send_message

now = timezone.now()

# Check last updates from each user
users = assistent_models.User.objects.filter(
    last_update__lte=now - timezone.timedelta(minutes=SEND_END_MESSAGE_MINUTES),
    end_messages_sent=False
)

# Send end messages
for user in users:
    
    # Get business and telegram token
    business = user.business
    telegram_token = socials_models.TelegramToken.objects.filter(
        business=business
    ).first()
    telegram_token_value = telegram_token.token
    end_message_1 = business.end_message_1
    end_message_2 = business.end_message_2
    messages = [end_message_1, end_message_2]
    
    # Send end messages
    for message in messages:
        if not message:
            message_index = messages.index(message)
            print(f"Business {business} has no end message {message_index + 1}")
            continue
        
        print(f"Sending end message {message} to user {user.key}")
        send_message(
            bot_token=telegram_token_value,
            user_key=user.key,
            message=message,
        )
        
    # Update user
    user.end_messages_sent = True
    user.save()