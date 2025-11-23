from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from extensions import db
from config import Config
from agent import get_response
from models import User, Doctor


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    # Create database tables
    with app.app_context():
        db.create_all()

    @app.route('/seed-doctors')
    def seed_doctors():
        doctors = [
            ("Dr. Amina Bello", "amina@hospital.com", "Obstetrics",
                "Lagos Island Maternity", "+2348012345671"),
            ("Dr. Kemi Johnson", "kemi@hospital.com", "Gynecology",
                "First Women Clinic", "+2348012345672"),
            ("Dr. Fatima Lawal", "fatima@hospital.com", "Reproductive Health",
                "Abuja Specialist Hospital", "+2348012345673"),
        ]

        for name, email, specialty, facility, phone in doctors:
            if User.query.filter_by(email=email).first():
                continue

            user = User(
                email=email,
                role="doctor",
                full_name=name
            )
            user.set_password("password123")
            db.session.add(user)
            db.session.flush()

            doctor = Doctor(
                user_id=user.id,
                specialty=specialty,
                facility=facility,
                phone=phone
            )

            db.session.add(doctor)

        db.session.commit()
        return {"message": "Doctors seeded"}

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
        print('data: ', data)
        message = data.get("message", "").strip()
        user_id = data.get("user_id", "user_001")

        if not message:
            return jsonify({"error": "No message provided"}), 400

        # Get AI response
        ai_reply = get_response(message, user_id=user_id)

        return jsonify({"response": ai_reply})

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
