# simple_ecommerce/User_Authentication/signup.py
import re

from testing_simple_ecommerce.simple_ecommerce import mock_db


class RegistrationError(Exception):
    pass


def signup(username, password, email):
    if mock_db is None:
        raise ValueError("mock_db is not injected.")

    if not username or not password or not email:
        raise RegistrationError("All fields are required.")
    if (
        not isinstance(username, str)
        or not isinstance(password, str)
        or not isinstance(email, str)
    ):
        raise RegistrationError("Invalid input type.")
    if len(username) > 150 or len(password) > 128 or len(email) > 255:
        raise RegistrationError("Input too long.")
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise RegistrationError("Invalid email format.")
    if re.search(r"[\"\'\\;<>]", username + password + email):
        raise RegistrationError("Potential injection detected.")
    if mock_db.username_exists(username):
        raise RegistrationError("Username already exists.")
    mock_db.add_user(username, password, email)
    return True
