from django.shortcuts import render

class TelegramChat():
    def post(self, request):
        print(f"Webhook received for {bot_name}")

        # Get message
        data = request.json
        message = data.get("message", "")

        # Return default confirmation message
        if not message:
            return {
                "status": "success",
                "message": "notification received",
                "data": []
            }

        # Get message part
        message_text = message["text"]
        message_chat_id = message["chat"]["id"]

        # Run main workflow
        # workflow_thread = Thread(
        #     target=bot.workflow,
        #     args=(message_text, message_chat_id, bot_name)
        # )
        # workflow_thread.start()

        # Return success
        return {
            "status": "success",
            "message": "message sent",
            "data": []
        }
