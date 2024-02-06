import os
from dotenv import load_dotenv
import requests

load_dotenv()
HOST = os.getenv("HOST")


def get_message_chatgpt(message: str, business: str, user_name: str,
                        user_key: str, user_origin: str) -> dict:
    """ Get data from assistent chatgpt api and return a dict with the data

    Args:
        message (str): user message
        business (str): bisiness name
        user_name (str): user usernmame in the chat platform
        user_key (str): user key in the chat platform
        user_origin (str): user chat platform (like telegram, whatsapp, etc.)

    Returns:
        touple: (bool, str)
            bools: True if the request was successful, False otherwise
            str: response message from chatgpt
    """

    # Format data
    data = {
        "message": message,
        "business": business,
        "user": {
            "name": user_name,
            "key": user_key,
            "origin": user_origin
        }
    }
    
    error_response = (False, "Servicio no disponible. Intente más tarde.")
    
    # Send post request
    url = f"{HOST}/api/chat/"
    res = requests.post(url, json=data)
    if res.status_code != 200:
        return error_response
    
    # Extract chatgpt message
    data = res.json()
    response = data.get("data", {}).get("response", "")
    if not response:
        return error_response
    
    return (True, response)