from app import db
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    name = db.Column(db.String(80), nullable=True)   # ✅ New: for profile update
    email = db.Column(db.String(120), unique=True, nullable=True)  # ✅ New: for profile update

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)

# Incident model
class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # Low, Medium, High
    status = db.Column(db.String(20), default='Open')    # Open, In Progress, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # 🔗 Assigned to user
    assigned_to_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    assigned_to = db.relationship('User', backref='assigned_incidents')

    # 🔖 Additional Fields
    priority = db.Column(db.String(20), nullable=True)
    tags = db.Column(db.String(120), nullable=True)
    notes = db.Column(db.Text, nullable=True)
