from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from server.database.tokens import generate_reset_token, verify_reset_token
from server.controllers.email_store import send_reset_email
from server.database.connect import get_db_connection
from argon2 import PasswordHasher

# Blueprint for password reset functionality
password_api = Blueprint('password_api', __name__)

# Initialize password hasher
ph = PasswordHasher()


@password_api.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    # Verify token and extract email
    email = verify_reset_token(token)

    # If token invalid or expired
    if not email:
        flash("The password reset link is invalid or has expired.", "danger")
        return redirect(url_for("login_api.login"))
    
    # Handle form submission (POST)
    if request.method == "POST":
        # Get new password from form
        new_password = request.form.get("password")

        # Validate input
        if not new_password:
            flash("Please enter a new password.", "warning")
            return render_template("reset_password.html", token=token)
        
        # Update password in database
        with get_db_connection() as conn:
            new_hash = ph.hash(new_password)  # hash new password
            conn.execute(
                "UPDATE user SET password_hash = ? WHERE email = ?",
                (new_hash, email)
            )
            conn.commit()
        
        # Notify user of success
        flash("Your password has been reset successfully. Please log in.", "success")

        # Redirect to login page
        return redirect(url_for("login_api.login"))
    
    # If GET request, render reset form
    return render_template("reset_password.html", token=token)


@password_api.route("/reset-password", methods=["POST"])
def request_password_reset():
    # Get JSON request body
    data = request.get_json(silent=True) or {}

    # Normalize email input
    email = (data.get("email") or "").strip().lower()

    # Always return generic success to avoid leaking whether an email exists
    if not email:
        return jsonify(success=False, error="Email is required."), 400

    # Check if user exists in database
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM [user] WHERE Email = ?", (email,))
        user_exists = cur.fetchone() is not None

    # If user exists, generate token and send email
    if user_exists:
        token = generate_reset_token(email)

        # Build reset link (absolute URL)
        reset_link = url_for("password_api.reset_password", token=token, _external=True)

        # Send reset email
        send_reset_email(email, reset_link)

    # Always return success regardless of user existence
    return jsonify(success=True)