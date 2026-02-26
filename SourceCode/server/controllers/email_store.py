import os
import resend
resend.api_key = os.getenv("RESEND_API_KEY")

def send_reset_email(user_email, reset_link):
    try:
        response = resend.Emails.send({
        "from": os.getenv("RESEND_FROM"),
        "to": [user_email],
        "subject": "Reset Your Password",
            "html": f"""
                <p>Click below to reset your password:</p>
                <a href="{reset_link}">Reset Password</a>
                <p>This link expires in 1 hour.</p>
            """
        })

        print("Email sent successfully:", response)
    except Exception as e:
        print("Error sending email:", e)
