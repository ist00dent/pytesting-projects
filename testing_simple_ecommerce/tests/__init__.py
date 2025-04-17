# tests/__init__.py
import pytest

from testing_simple_ecommerce.simple_ecommerce.User_Authentication.signup import signup

VALID_USERNAME = "valid_user"
VALID_PASSWORD = "ValidPass123!"
VALID_EMAIL = "valid_user@example.com"


def get_valid_user_credentials():
    return VALID_USERNAME, VALID_PASSWORD, VALID_EMAIL


@pytest.fixture
def test_signup_valid():
    username, password, email = get_valid_user_credentials()
    assert signup(username, password, email) is True
