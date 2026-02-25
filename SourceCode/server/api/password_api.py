from flask import Blueprint, request, render_template, redirect, url_for, flash
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
            conn.execute("UPDATE users SET password_hash = ? WHERE email = ?", (new_hash, email))
            conn.commit()
        
        flash("Your password has been reset successfully. Please log in.", "success")
        return redirect(url_for("login_api.login"))
    
    return render_template("reset_password.html", token=token)
