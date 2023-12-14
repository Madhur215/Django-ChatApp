# chat/services.py
import logging
from .models import Messages


class MessageService:
    @staticmethod
    def create_message_and_automatic_response(sender, receiver, content):
        # Create the original message
        original_message = Messages.objects.create(sender=sender, receiver=receiver, content=content)

        # Create the automatic response
        automatic_response_content = "Thank you for your message! This is an automatic response."
        automatic_response = Messages.objects.create(
            sender=receiver,
            receiver=sender,
            content=automatic_response_content,
        )

        # Log information for debugging
        logging.info(f"Original message created: {original_message}")
        logging.info(f"Automatic response created: {automatic_response}")

        # You can perform additional actions if needed

        return original_message

