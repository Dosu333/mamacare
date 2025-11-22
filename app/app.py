from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from utils.ai_engine import classify_intent
from utils.parse_json import safe_parse_json


app = Flask(__name__)


@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.form.get("Body", "").strip()
    resp = MessagingResponse()
    msg = resp.message()

    result = classify_intent(incoming_msg)
    intent_data = safe_parse_json(result)
    intent = intent_data.get("intent", "UNSURE")

    if intent == "STATUS":
        msg.body("Here is your latest health update. (vitals & appointments placeholder)")
    elif intent == "REPORT_SYMPTOM":
        msg.body("Thank you for sharing. Can you tell me if you also have dizziness, swelling, or blurred vision?")
    elif intent == "CYCLE_START":
        msg.body("Got it. I’ve logged the start of your cycle and will track it for you.")
    elif intent == "PREGNANCY_ANNOUNCE":
        msg.body("Congratulations! I can start giving you weekly pregnancy tips. How many weeks along are you?")
    elif intent == "REQUEST_REPORT":
        msg.body("Sure, I can create a report for you and your doctor.")
    elif intent == "SMALL_TALK":
        msg.body("You’re welcome! How can I help you today?")
    else:
        msg.body("I’m here to support you. Can you tell me more about how you’re feeling today?")

    return str(resp)


if __name__ == "__main__":
    app.run(debug=True)
