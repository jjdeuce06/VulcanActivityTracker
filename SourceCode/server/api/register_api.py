from flask import Blueprint, request, jsonify
from controllers.email_store import send_verification_email
from database.tokens import generate_email_verification_token

register_api = Blueprint("register_api", __name__)


@register_api.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    if not email or not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # TODO:
    # 1. check if user already exists
    # 2. hash password
    # 3. save user in DB with IsVerified = 0

    try:
        token = generate_email_verification_token(email)
        send_verification_email(email, token)
    except Exception as e:
        print("Error sending verification email:", e)
        return jsonify({"error": "User created, but verification email failed to send"}), 500

    return jsonify({"message": "Registration successful. Verification email sent."}), 201