from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "").strip().lower()

    resp = MessagingResponse()
    msg = resp.message()

    if "hello" in incoming_msg:
        msg.body("Hello, I am MamaCare 💙 I am here to support your health.")

    elif "help" in incoming_msg:
        msg.body("Sure! You can tell me how you're feeling or ask about your health.")

    else:
        msg.body("I’m here for you. Can you tell me more about how you’re feeling today?")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
