from flask import Blueprint, request, jsonify
from argon2 import PasswordHasher

from server.controllers.email_store import send_password_reset_email
from server.database.tokens import (
    generate_password_reset_token,
    confirm_password_reset_token
)
from server.database.connect import get_db_connection
from server.controllers.login_store import (
    fetch_user_by_email,
    update_password_by_email
)

password_api = Blueprint("password_api", __name__)


@password_api.route("/forgot-password", methods=["POST"])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email is required"}), 400

    try:
        with get_db_connection() as conn:
            user = fetch_user_by_email(conn, email)

        # Only send email if the user exists,
        # but still return the same response either way
        if user:
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

    try:
        ph = PasswordHasher()
        hashed_password = ph.hash(new_password)

        with get_db_connection() as conn:
            updated = update_password_by_email(conn, email, hashed_password)

        if not updated:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"message": "Password reset successful"}), 200

    except Exception as e:
        print("Error resetting password:", e)
        return jsonify({"error": "Failed to reset password"}), 500