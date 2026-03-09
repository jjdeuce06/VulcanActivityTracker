from flask import Blueprint, jsonify
from database.tokens import confirm_email_verification_token

verify_api = Blueprint("verify_api", __name__)


@verify_api.route("/verify-email/<token>", methods=["GET"])
def verify_email(token):
    email = confirm_email_verification_token(token)

    if not email:
        return jsonify({"error": "Invalid or expired verification token"}), 400

    # TODO:
    # Update DB:
    # set IsVerified = 1 where Email = email

    return jsonify({"message": "Email verified successfully"}), 200