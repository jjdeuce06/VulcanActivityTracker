from flask import Blueprint, request, jsonify
from controllers.email_store import send_password_reset_email
from database.tokens import generate_password_reset_token

password_api = Blueprint("password_api", __name__)


@password_api.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # TODO:
    # Check whether user exists in DB
    # If user does not exist, you may still return success to avoid user enumeration

    try:
        token = generate_password_reset_token(email)
        send_password_reset_email(email, token)
    except Exception as e:
        print("Error sending password reset email:", e)
        return jsonify({"error": "Failed to send password reset email"}), 500

    return jsonify({"message": "If that email exists, a password reset link has been sent."}), 200

@password_api.route("/reset-password/<token>", methods=["POST"])
def reset_password(token):
    data = request.get_json()
    new_password = data.get("password")

    if not new_password:
        return jsonify({"error": "Password is required"}), 400

    email = confirm_password_reset_token(token)
    if not email:
        return jsonify({"error": "Invalid or expired reset token"}), 400

    hashed_password = generate_password_hash(new_password)

    # TODO:
    # Update DB:
    # set PasswordHash = hashed_password where Email = email

    return jsonify({"message": "Password reset successful"}), 200