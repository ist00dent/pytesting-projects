# simple_ecommerce/User_Authentication/login.py
import re

from testing_simple_ecommerce.simple_ecommerce import mock_db


class AuthenticationError(Exception):
    pass


def login(username, password):
    if mock_db is None:
        raise ValueError("mock_db is not injected.")

    if not username or not password:
        raise AuthenticationError("Username and password are required.")
    if not isinstance(username, str) or not isinstance(password, str):
        raise AuthenticationError("Invalid input type.")
    if len(username) > 150 or len(password) > 128:
        raise AuthenticationError("Input too long.")
    if re.search(r"[\"\'\\;<>]", username) or re.search(r"[\"\'\\;<>]", password):
        raise AuthenticationError("Potential injection detected.")

    mock_db.increment_login_attempts(username)
    if mock_db.get_login_attempts(username) > 5:
        raise AuthenticationError("Too many failed login attempts.")
    return True
