import json
import requests


def send_message(bot_token: str, user_key: str, message: str):
    """ Send message to specific user in telegram

    Args:
        bot_token (str): telegram bot token
        user_key (str): user key in the chat platform
        message (str): user message
    """
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": user_key,
        "text": message,
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json"
    }
    res = requests.post(url, data=json_data, headers=headers)
    res.raise_for_status()


def send_message_chatgpt(message: str, business: str, user_name: str,
                         user_key: str, user_origin: str, bot_token: str,
                         chatbot_class: object, models_class: object) -> dict:
    """ Get data from assistent chatgpt api and send message to the user

    Args:
        message (str): user message
        business (str): bisiness name
        user_name (str): user usernmame in the chat platform
        user_key (str): user key in the chat platform
        user_origin (str): user chat platform (like telegram, whatsapp, etc.)
        bot_token (str): telegram bot token
    """
    
    chatbot = chatbot_class(
        models_class.Business.objects.all(),
        models_class.Instruction.objects.all(),
    )
    
    reponse = chatbot.workflow(
        message=message,
        business_name=business,
        user_key=user_key,
        user_origin=user_origin,
        user_name=user_name
    )
    
    log = f"Sending message from {business} to {user_key}: {reponse}"
    print(log)
    
    send_message(bot_token, user_key, reponse)

    

    
