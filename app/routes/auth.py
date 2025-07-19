from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({"msg": "Username and password are required"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(
        username=data['username'],
        password_hash=User.generate_hash(data['password'])
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()

    if not user or not User.verify_hash(data['password'], user.password_hash):
        return jsonify({"msg": "Bad username or password"}), 401

    token = create_access_token(identity=user.username)
    return jsonify(access_token=token)

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    current_username = get_jwt_identity()
    user = User.query.filter_by(username=current_username).first()

    if not user:
        return jsonify({"msg": "User not found"}), 404

    data = request.get_json()

    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({'msg': 'Profile updated'})
