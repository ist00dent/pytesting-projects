# test_password_reset.py
import pytest
from testing_simple_ecommerce.simple_ecommerce.User_Authentication.password_reset import (
    request_password_reset,
    reset_password,
    PasswordResetError,
)
from testing_simple_ecommerce.tests import VALID_EMAIL


def test_password_reset_valid_flow():
    token = request_password_reset(VALID_EMAIL)
    assert reset_password(VALID_EMAIL, token) is True


@pytest.mark.parametrize(
    "email", ["", None, 123, "invalid-email", "plainaddress", "@missinguser.com"]
)
def test_password_reset_invalid_email_format(email):
    with pytest.raises(PasswordResetError):
        request_password_reset(email)


def test_password_reset_invalid_token():
    token = "invalid-token"
    with pytest.raises(PasswordResetError):
        reset_password(VALID_EMAIL, token)


def test_password_reset_nonexistent_email():
    with pytest.raises(PasswordResetError):
        request_password_reset("nonexistent@example.com")


def test_password_reset_missing_token():
    with pytest.raises(PasswordResetError):
        reset_password(VALID_EMAIL, None)


def test_password_reset_missing_email():
    token = request_password_reset(VALID_EMAIL)
    with pytest.raises(PasswordResetError):
        reset_password(None, token)
