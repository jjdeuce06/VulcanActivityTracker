import os
from itsdangerous import URLSafeTimedSerializer

def _serializer():
    return URLSafeTimedSerializer(os.getenv("SECRET_KEY"))

def generate_reset_token(email):
    return _serializer().dumps(email, salt="password-reset-salt")

def verify_reset_token(token, expiration=3600):
    try:
        return _serializer().loads(token, salt="password-reset-salt", max_age=expiration)
    except Exception:
        return None