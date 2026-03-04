from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from server.database.tokens import generate_reset_token, verify_reset_token
from server.controllers.email_store import send_reset_email
from server.database.connect import get_db_connection
from argon2 import PasswordHasher


password_api = Blueprint('password_api', __name__)
ph = PasswordHasher()

@password_api.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("The password reset link is invalid or has expired.", "danger")
        return redirect(url_for("login_api.login"))
    
    if request.method == "POST":
        new_password = request.form.get("password")
        if not new_password:
            flash("Please enter a new password.", "warning")
            return render_template("reset_password.html", token=token)
        
        with get_db_connection() as conn:
            new_hash = ph.hash(new_password)
            conn.execute("UPDATE user SET password_hash = ? WHERE email = ?", (new_hash, email))
            conn.commit()
        
        flash("Your password has been reset successfully. Please log in.", "success")
        return redirect(url_for("login_api.login"))
    
    return render_template("reset_password.html", token=token)

@password_api.route("/reset-password", methods=["POST"])
def request_password_reset():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()

    # Always return generic success to avoid leaking whether an email exists
    if not email:
        return jsonify(success=False, error="Email is required."), 400

    # Check if user exists (adjust column/table names if needed)
    with get_db_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM [user] WHERE Email = ?", (email,))
        user_exists = cur.fetchone() is not None

    if user_exists:
        token = generate_reset_token(email)
        reset_link = url_for("password_api.reset_password", token=token, _external=True)
        send_reset_email(email, reset_link)

    return jsonify(success=True)