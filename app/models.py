from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(254), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'doctor', 'admin'
    full_name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)


class Doctor(db.Model):
    __tablename__ = "doctors"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    specialty = db.Column(db.String(128))
    facility = db.Column(db.String(128))
    phone = db.Column(db.String(30))
    user = db.relationship("User", backref="doctor_profile")


class Patient(db.Model):
    __tablename__ = "patients"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(200))
    phone = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(254), nullable=True)
    date_of_birth = db.Column(db.Date)
    is_pregnant = db.Column(db.Boolean, default=False)
    pregnancy_start = db.Column(db.Date, nullable=True)
    last_cycle_start = db.Column(db.Date, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Cycle(db.Model):
    __tablename__ = "cycles"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer, nullable=False
    )
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=True)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Observation(db.Model):
    __tablename__ = "observations"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50))  # e.g., "menstrual_cycle_start",..."
    value = db.Column(db.String(200))  # e.g., "Cycle started", "Pregnant"
    unit = db.Column(db.String(50), nullable=True)  # e.g., "bpm", "Celsius"
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)
    source = db.Column(db.String(50), default="whatsapp")


class Appointment(db.Model):
    __tablename__ = "appointments"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer, db.ForeignKey("patients.id"), nullable=False
    )
    doctor_id = db.Column(
        db.Integer, db.ForeignKey("doctors.id"), nullable=True
    )
    date = db.Column(db.DateTime, nullable=False)
    reason = db.Column(db.String(500))
    status = db.Column(
        db.String(20), default="active"
    )  # active, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship("Patient")
    doctor = db.relationship("Doctor")


class ChatMessage(db.Model):
    __tablename__ = "chat_messages"
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(
        db.Integer, db.ForeignKey("patients.id"), nullable=True
    )
    sender = db.Column(db.String(20))  # 'patient', 'bot', 'doctor'
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    patient = db.relationship("Patient")


class Drug(db.Model):
    __tablename__ = "drugs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=True)
    notes = db.Column(db.Text)
    pregnancy_safe = db.Column(db.Boolean, default=True)


class DrugInteraction(db.Model):
    __tablename__ = "drug_interactions"
    id = db.Column(db.Integer, primary_key=True)
    drug_a_id = db.Column(db.Integer, db.ForeignKey("drugs.id"))
    drug_b_id = db.Column(db.Integer, db.ForeignKey("drugs.id"))
    severity = db.Column(db.String(20))  # Major/Moderate/Minor
    note = db.Column(db.Text)
