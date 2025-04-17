# test_login.py
import pytest
from testing_simple_ecommerce.simple_ecommerce.User_Authentication.login import (
    login,
    AuthenticationError,
)
from testing_simple_ecommerce.tests import get_valid_user_credentials


def test_login_valid():
    username, password, _ = get_valid_user_credentials()
    assert login(username, password) is True


@pytest.mark.parametrize(
    "username,password",
    [
        ("", "pass"),
        ("user", ""),
        (None, "pass"),
        ("user", None),
        (123, "password"),
        ("user", 456),
    ],
)
def test_login_invalid_input(username, password):
    with pytest.raises(AuthenticationError):
        login(username, password)


@pytest.mark.parametrize(
    "username,password",
    [
        ("admin';--", "password"),
        ("user", "' OR '1'='1"),
        ("user<script>", "password"),
        ("user", "<script>alert(1)</script>"),
        ("user; DROP TABLE users;", "password"),
    ],
)
def test_login_injection_detection(username, password):
    with pytest.raises(AuthenticationError):
        login(username, password)


@pytest.mark.parametrize(
    "username,password",
    [
        ("user!@#$%^&*()", "password123"),
        ("user_name", "pass$%^&*()"),
        ("🚀user", "p@ssw0rd"),
    ],
)
def test_login_special_characters(username, password):
    try:
        assert login(username, password) is True
    except AuthenticationError:
        pass
