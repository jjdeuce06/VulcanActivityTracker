import os
import resend
resend.api_key = os.getenv("RESEND_API_KEY")

def send_reset_email(user_email, reset_link):
    resend.Emails.send({
    "from": os.getenv("RESEND_FROM"),
    "to": user_email,
    "subject": "Reset Your Password",
        "html": f"""
            <p>Click below to reset your password:</p>
            <a href="{reset_link}">Reset Password</a>
            <p>This link expires in 1 hour.</p>
        """
    })