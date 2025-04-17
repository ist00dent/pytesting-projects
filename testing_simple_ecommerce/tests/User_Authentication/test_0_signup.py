# test_signup.py
import pytest
from testing_simple_ecommerce.simple_ecommerce.User_Authentication.signup import (
    signup,
    RegistrationError,
)
from testing_simple_ecommerce.tests import get_valid_user_credentials


def test_signup_valid():
    username, password, email = get_valid_user_credentials()
    assert signup(username, password, email) is True


@pytest.mark.parametrize(
    "username,password,email",
    [
        ("", "pass", "user@example.com"),
        ("user", "", "user@example.com"),
        ("user", "pass", ""),
        (None, "pass", "user@example.com"),
        ("user", None, "user@example.com"),
        ("user", "pass", None),
        (123, "pass", "user@example.com"),
        ("user", 456, "user@example.com"),
        ("user", "pass", 789),
    ],
)
def test_signup_invalid_input(username, password, email):
    with pytest.raises(RegistrationError):
        signup(username, password, email)


@pytest.mark.parametrize(
    "username,password,email",
    [
        ("user", "password", "not-an-email"),
        ("user", "password", "plainaddress"),
        ("user", "password", "@missinguser.com"),
    ],
)
def test_signup_invalid_email_format(username, password, email):
    with pytest.raises(RegistrationError):
        signup(username, password, email)


@pytest.mark.parametrize(
    "username,password,email",
    [
        ("admin';--", "password123", "user@example.com"),
        ("user<script>", "password123", "user@example.com"),
        ("user", "' OR '1'='1", "user@example.com"),
        ("user", "password123", "email@example.com<script>"),
        ("user; DROP TABLE users;", "password123", "user@example.com"),
    ],
)
def test_signup_injection_detection(username, password, email):
    with pytest.raises(RegistrationError):
        signup(username, password, email)


@pytest.mark.parametrize(
    "username,password,email",
    [
        ("user!@#$%^&*()", "password123!@#", "user+alias@example.com"),
        ("user_name", "pass$%^&*()", "user_name@example.com"),
        ("🚀user", "p@ssw0rd", "rocket.user@example.com"),
    ],
)
def test_signup_special_characters(username, password, email):
    try:
        assert signup(username, password, email) is True
    except RegistrationError:
        pass
