# simple_ecommerce/User_Authentication/password_reset.py
import re

from testing_simple_ecommerce.simple_ecommerce import mock_db


class PasswordResetError(Exception):
    pass


def request_password_reset(email):
    if mock_db is None:
        raise ValueError("mock_db is not injected.")

    if not email or not isinstance(email, str):
        raise PasswordResetError("Invalid email.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise PasswordResetError("Invalid email format.")
    if not mock_db.email_exists(email):
        raise PasswordResetError("Email not registered.")
    token = mock_db.generate_reset_token(email)
    return token


def reset_password(email, token):
    if not email or not token:
        raise PasswordResetError("Email and token are required.")
    if not mock_db.verify_reset_token(email, token):
        raise PasswordResetError("Invalid or expired token.")
    return True
