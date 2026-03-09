import os
import requests

MAILERSEND_API_KEY = os.getenv("MAILERSEND_API_KEY")
MAIL_FROM_EMAIL = os.getenv("MAIL_FROM_EMAIL")
MAIL_FROM_NAME = os.getenv("MAIL_FROM_NAME", "Vulcan Activity Tracker")

MAILERSEND_URL = "https://api.mailersend.com/v1/email"


def send_email(to_email, subject, html_content, text_content=None):
    """
    Sends an email using the MailerSend API.
    Raises an exception if sending fails.
    """
    if not MAILERSEND_API_KEY:
        raise ValueError("MAILERSEND_API_KEY is not set")
    if not MAIL_FROM_EMAIL:
        raise ValueError("MAIL_FROM_EMAIL is not set")

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

    response = requests.post(
        MAILERSEND_URL,
        json=payload,
        headers=headers,
        timeout=15
    )

    if response.status_code not in (200, 202):
        raise Exception(
            f"MailerSend error {response.status_code}: {response.text}"
        )

    return response.json() if response.text else {"status": "accepted"}

FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL", "http://localhost:6455")


def send_verification_email(to_email, token):
    verify_link = f"{FRONTEND_BASE_URL}/verify-email/{token}"

    subject = "Verify your Vulcan Activity Tracker account"

    html_content = f"""
    <h2>Verify your account</h2>
    <p>Welcome to Vulcan Activity Tracker.</p>
    <p>Please click the link below to verify your email address:</p>
    <p><a href="{verify_link}">Verify Email</a></p>
    <p>If you did not create this account, you can ignore this email.</p>
    """

    text_content = (
        f"Welcome to Vulcan Activity Tracker.\n\n"
        f"Verify your email here:\n{verify_link}\n\n"
        f"If you did not create this account, you can ignore this email."
    )

    return send_email(to_email, subject, html_content, text_content)


def send_password_reset_email(to_email, token):
    reset_link = f"{FRONTEND_BASE_URL}/password_api/reset-password/{token}"

    subject = "Reset your Vulcan Activity Tracker password"

    html_content = f"""
    <h2>Password Reset Request</h2>
    <p>We received a request to reset your password.</p>
    <p>Click the link below to choose a new password:</p>
    <p><a href="{reset_link}">Reset Password</a></p>
    <p>If you did not request this, you can safely ignore this email.</p>
    """

    text_content = (
        f"We received a request to reset your password.\n\n"
        f"Reset it here:\n{reset_link}\n\n"
        f"If you did not request this, you can safely ignore this email."
    )

    return send_email(to_email, subject, html_content, text_content)