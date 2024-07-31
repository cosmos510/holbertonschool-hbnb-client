from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from db import db
from models.users import User
from werkzeug.security import check_password_hash
from flask_jwt_extended import jwt_required, get_jwt_identity


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=["POST"])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    user = User.query.filter_by(email=email).first()
    additional_claims = {"is_admin": user.is_admin}
    if user:
        if check_password_hash(user.password, password):
            access_token = create_access_token(
                identity={'username': email, 'role': user.is_admin}, additional_claims=additional_claims)
            return jsonify(access_token=access_token)
    return jsonify({"error": "Invalid credentials"}), 401
