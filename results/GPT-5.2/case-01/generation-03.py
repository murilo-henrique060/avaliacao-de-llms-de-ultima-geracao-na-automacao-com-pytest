import pytest

# NOTE:
# These tests assume the SUT provides `UserService` (and returns a `User`) as specified.
# Adjust the import path to match your project structure.
from cases.case01 import UserService  # type: ignore


def test_register_allows_creating_user_with_name_email_password_returns_user():
    # FR01 – The system must allow registering a user
    service = UserService()

    user = service.register(name="Alice", email="alice@example.com", password="secret")

    assert user is not None


def test_register_valid_data_creates_user_with_expected_name():
    # BR01 – All users must have a name, email, and password
    service = UserService()

    user = service.register(name="Bob", email="bob@example.com", password="secret")

    assert user.name == "Bob"


def test_register_missing_name_raises_exception():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="", email="noname@example.com", password="secret")


def test_register_missing_email_raises_exception():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="NoEmail", email="", password="secret")


def test_register_missing_password_raises_exception():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="NoPassword", email="nopassword@example.com", password="")


def test_register_email_with_at_character_is_accepted():
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    service = UserService()

    user = service.register(name="Carol", email="carol@domain.com", password="secret")

    assert user is not None


def test_register_email_without_at_character_raises_exception():
    # BR02 – The email must contain the @ character
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Dave", email="davedomain.com", password="secret")


def test_register_password_with_exactly_6_characters_is_accepted():
    # BR03 – The password must have at least 6 characters
    service = UserService()

    user = service.register(name="Eve", email="eve@example.com", password="123456")

    assert user is not None


def test_register_password_with_5_characters_raises_exception():
    # BR03 – The password must have at least 6 characters
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Frank", email="frank@example.com", password="12345")


def test_register_duplicate_email_raises_exception():
    # BR04 – It is not allowed to register two users with the same email
    # FR03 – The system must prevent registration with a duplicate email
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    service.register(name="Grace", email="dup@example.com", password="secret")

    with pytest.raises(Exception):
        service.register(name="Heidi", email="dup@example.com", password="secret")