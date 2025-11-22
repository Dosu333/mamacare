from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()


def send_whatsapp_message(to, body):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to=f'whatsapp:{to}'
        )

    return message.sid
