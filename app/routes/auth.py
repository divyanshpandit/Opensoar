from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

# GET: Show register form, POST: Handle register
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')  # ✅ Make sure register.html exists

    # Handle form submission
    data = request.form
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 400

    new_user = User(
        username=username,
        password_hash=User.generate_hash(password)
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))  # redirect to login after registration


# GET: Show login form, POST: Handle login
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')  # ✅ Make sure login.html exists

    data = request.form
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not User.verify_hash(password, user.password_hash):
        return jsonify({"msg": "Bad username or password"}), 401

    token = create_access_token(identity=user.username)
    return jsonify(access_token=token)


# Profile update route
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
        user.password_hash = User.generate_hash(data['password'])

    db.session.commit()
    return jsonify({'msg': 'Profile updated'})
