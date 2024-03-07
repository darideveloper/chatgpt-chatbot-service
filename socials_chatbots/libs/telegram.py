import json
import requests


def set_typing(bot_token: str, user_key: str):

    url = f"https://api.telegram.org/bot{bot_token}/sendChatAction"

    payload = json.dumps({
        "chat_id": user_key,
        "action": "typing"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request(
        "POST",
        url,
        headers=headers,
        data=payload
    )

    print(response.text)


def send_message(bot_token: str, user_key: str, message: str,
                 keyboard: dict = {}, keyboard_text: str = ""):
    """ Send message to specific user in telegram

    Args:
        bot_token (str): telegram bot token
        user_key (str): user key in the chat platform
        message (str): user message
        keyboard (dict): keyboard to send to the user
    """
    
    # Add select category to message
    if keyboard and keyboard_text:
        message += f"\n\n{keyboard_text}"
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": user_key,
        "text": message,
        "reply_markup": keyboard,
    }
    json_data = json.dumps(data)
    print(data)
    headers = {
        "Content-Type": "application/json"
    }
    res = requests.post(url, data=json_data, headers=headers)
    res.raise_for_status()


def load_products(business: str, user_name: str,
                  user_key: str, user_origin: str,
                  chatbot_class: object, models_class: object,
                  products: object, openai_apikey: str):
    """ Create a new user chat and load specific category products
    
    Args:
        business (str): bisiness name
        user_name (str): user usernmame in the chat platform
        user_key (str): user key in the chat platform
        user_origin (str): user chat platform (like telegram, whatsapp, etc.)
        chatbot_class (object): chatbot class
        models_class (object): models class
        products (object): products from the business
        openai_apikey (str): openai api key
    """
    
    chatbot = chatbot_class(
        models_class.Business,
        models_class.Instruction,
        openai_apikey,
    )
    
    chatbot.load_products(
        user_key=user_key,
        user_origin=user_origin,
        user_name=user_name,
        business_name=business,
        products_objs=products
    )


def send_message_chatgpt(message: str, business: str, user_name: str,
                         user_key: str, user_origin: str, bot_token: str,
                         chatbot_class: object, models_class: object,
                         keyboard: dict, openai_apikey: str) -> dict:
    """ Get data from assistent chatgpt api and send message to the user

    Args:
        message (str): user message
        business (str): bisiness name
        user_name (str): user usernmame in the chat platform
        user_key (str): user key in the chat platform
        user_origin (str): user chat platform (like telegram, whatsapp, etc.)
        bot_token (str): telegram bot token
        keyboard (dict): keyboard to send to the user
        products (object): products from the business
    """
    
    chatbot = chatbot_class(
        models_class.Business,
        models_class.Instruction,
        openai_apikey,
    )
    
    reponse = chatbot.workflow(
        message=message,
        business_name=business,
        user_key=user_key,
        user_origin=user_origin,
        user_name=user_name,
    )
    
    log = f"Sending message from {business} to {user_key}: {reponse}"
    print(log)
    
    send_message(bot_token, user_key, reponse, keyboard)

    

    
