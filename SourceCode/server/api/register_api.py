from flask import Blueprint, request, jsonify
from controllers.email_store import send_verification_email
from database.tokens import generate_email_verification_token

# Blueprint for user registration routes
register_api = Blueprint("register_api", __name__)


@register_api.route("/register", methods=["POST"])
def register():
    # Get request data
    data = request.get_json()

    # Extract fields from request
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")

    # Validate required fields
    if not email or not username or not password:
        return jsonify({"error": "Missing required fields"}), 400

    # TODO:
    # 1. check if user already exists
    # 2. hash password
    # 3. save user in DB with IsVerified = 0

    try:
        # Generate email verification token
        token = generate_email_verification_token(email)

        # Send verification email to user
        send_verification_email(email, token)

    except Exception as e:
        # Handle email sending failure
        print("Error sending verification email:", e)
        return jsonify({"error": "User created, but verification email failed to send"}), 500

    # Return success response
    return jsonify({"message": "Registration successful. Verification email sent."}), 201