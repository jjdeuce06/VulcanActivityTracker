import os
from itsdangerous import URLSafeTimedSerializer


# ---------------- CREATE SERIALIZER ----------------
# Initializes a serializer using the app's secret key
def _serializer():
    return URLSafeTimedSerializer(os.getenv("SECRET_KEY"))


# ---------------- GENERATE RESET TOKEN ----------------
# Creates a secure, time-based token containing the user's email
def generate_reset_token(email):
    return _serializer().dumps(email, salt="password-reset-salt")


# ---------------- VERIFY RESET TOKEN ----------------
# Validates a token and returns the email if valid and not expired
def verify_reset_token(token, expiration=3600):
    try:
        # Attempt to decode token with expiration check (default 1 hour)
        return _serializer().loads(token, salt="password-reset-salt", max_age=expiration)
    except Exception:
        # Return None if token is invalid or expired
        return None