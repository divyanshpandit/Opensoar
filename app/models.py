from app import db
from passlib.hash import pbkdf2_sha256 as sha256

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash_):
        return sha256.verify(password, hash_)
from datetime import datetime
from app import db

class Incident(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # e.g., Low, Medium, High
    status = db.Column(db.String(20), default='Open')    # Open, In Progress, Closed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
