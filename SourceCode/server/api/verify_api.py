from flask import Blueprint, jsonify
from database.tokens import confirm_email_verification_token

# Blueprint for email verification routes
verify_api = Blueprint("verify_api", __name__)


@verify_api.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    # Validate token and extract associated email
    email = confirm_email_verification_token(token)

    # If token is invalid or expired
    if not email:
        return jsonify({"error": "Invalid or expired verification token"}), 400

    # TODO:
    # Update DB:
    # set IsVerified = 1 where Email = email

    # Return success response
    return jsonify({"message": "Email verified successfully"}), 200