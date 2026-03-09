import os
import requests

MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
MAIL_FROM_EMAIL = os.getenv("MAIL_FROM_EMAIL")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Vulcan Activity Tracker")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:6455")


def send_email(to_email, subject, html_content, text_content=None):
    if not MAILERSEND_API_KEY:
        raise ValueError("MAILERSEND_API_KEY is not set")
    if not MAIL_FROM_EMAIL:
        raise ValueError("MAIL_FROM_EMAIL is not set")

    url = "https://api.mailersend.com/v1/email"

    payload = {
        "from": {
            "email": MAIL_FROM_EMAIL,
            "name": MAIL_FROM_NAME
        },
        "to": [
            {
                "email": to_email
            }
        ],
        "subject": subject,
        "html": html_content
    }

    if text_content:
        payload["text"] = text_content

    headers = {
        "Authorization": f"Bearer {MAILERSEND_API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers, timeout=15)

    if response.status_code not in (200, 202):
        raise Exception(f"MailerSend error {response.status_code}: {response.text}")

    return response


def send_password_reset_email(to_email, token):
    reset_link = f"{FRONTEND_BASE_URL}/reset-password/{token}"

    subject = "Reset your Vulcan Activity Tracker password"

    html_content = f"""
    <h2>Password Reset</h2>
    <p>You requested a password reset.</p>
    <p>Click the link below to reset your password:</p>
    <p><a href="{reset_link}">Reset Password</a></p>
    <p>If you did not request this, you can ignore this email.</p>
    """

    text_content = f"""
You requested a password reset.

Use this link to reset your password:
{reset_link}

If you did not request this, you can ignore this email.
"""

    return send_email(to_email, subject, html_content, text_content)