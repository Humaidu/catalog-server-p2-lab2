from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from extensions import db
from models import User

auth_bp = Blueprint("auth", __name__)

# Login endpoint — accepts JSON credentials
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # Basic validation
    if not username or not password:
        return jsonify({"msg": "Username and password are required"}), 400

    # Find user in DB
    user = User.query.filter_by(username=username, password=password).first()
    if not user:
        return jsonify({"msg": "Invalid credentials"}), 401

    # Generate JWT access token
    access_token = create_access_token(identity=username)

    # Set token in cookie and return success
    response = jsonify({"msg": "Login successful"})
    set_access_cookies(response, access_token)
    return response

# Logout endpoint — clears cookie
@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"msg": "Logged out"})
    unset_jwt_cookies(response)
    return response

