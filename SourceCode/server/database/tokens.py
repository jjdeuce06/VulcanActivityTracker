from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from flask import current_app


def get_serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"])


def generate_email_verification_token(email):
    serializer = get_serializer()
    return serializer.dumps(email, salt="email-verification")


def confirm_email_verification_token(token, max_age=3600):
    serializer = get_serializer()
    try:
        email = serializer.loads(token, salt="email-verification", max_age=max_age)
        return email
    except (SignatureExpired, BadSignature):
        return None


def generate_password_reset_token(email):
    serializer = get_serializer()
    return serializer.dumps(email, salt="password-reset")


def confirm_password_reset_token(token, max_age=3600):
    serializer = get_serializer()
    try:
        email = serializer.loads(token, salt="password-reset", max_age=max_age)
        return email
    except (SignatureExpired, BadSignature):
        return None