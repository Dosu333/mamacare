from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from extensions import db
from config import Config
from agent import get_response


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    # Define routes inside create_app
    @app.route("/whatsapp", methods=["POST"])
    def whatsapp_reply():
        """
        Receives WhatsApp messages via Twilio and returns AI responses.
        """
        incoming_msg = request.form.get("Body", "").strip()
        user_phone = request.form.get("From", None)
        user_id = user_phone.split(':')[-1] or "+2347056918098"

        print('phone: ', user_phone.split(':')[-1])

        # Get AI response
        ai_reply = get_response(incoming_msg, user_id=user_id)

        # Respond via Twilio
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(ai_reply)

        return str(resp)

    @app.route("/chat", methods=["POST"])
    def chat_api():
        """
        General chat API for web/mobile clients.
        """
        data = request.json
        message = data.get("message", "").strip()
        user_id = data.get("phone", "user_001")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Get AI response
        ai_reply = get_response(message, user_id=user_id)

        return jsonify({"response": ai_reply})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
