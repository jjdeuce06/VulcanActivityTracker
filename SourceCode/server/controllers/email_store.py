import os
import resend

# Set API key for Resend email service from environment variables
resend.api_key = os.getenv("RESEND_API_KEY")


# ---------------- SEND PASSWORD RESET EMAIL ----------------
# Sends a password reset email with a secure reset link
def send_reset_email(user_email, reset_link):

    # Debug log before sending
    print(f"Preparing to send password reset email to {user_email} with link: {reset_link}")

    try:
        # Send email using Resend API
        response = resend.Emails.send({
            "from": os.getenv("RESEND_FROM"),  # sender email (must be verified)
            "to": [user_email],                # recipient email
            "subject": "Reset Your Password",  # email subject
            "html": f"""
                <p>Click below to reset your password:</p>
                <a href="{reset_link}">Reset Password</a>
                <p>This link expires in 1 hour.</p>
            """
        })

        # Log success response
        print("Email sent successfully:", response)

    except Exception as e:
        # Log any errors during email sending
        print("Error sending email:", e)