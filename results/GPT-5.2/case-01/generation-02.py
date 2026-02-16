import pytest

# NOTE:
# These tests assume the SUT provides the classes `User` and `UserService`
# with the exact public API described in the specification.
# Adjust the import path below to match your project structure.
from cases.case01 import UserService, User


def test_register_returns_user_instance_on_success():
    # FR01 – The system must allow registering a user
    service = UserService()

    user = service.register(name="Alice", email="alice@example.com", password="secret1")

    assert isinstance(user, User)


def test_register_raises_exception_when_name_missing():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="", email="alice@example.com", password="secret1")


def test_register_raises_exception_when_email_missing():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Alice", email="", password="secret1")


def test_register_raises_exception_when_password_missing():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Alice", email="alice@example.com", password="")


def test_register_accepts_user_when_all_required_fields_present():
    # BR01 – All users must have a name, email, and password
    service = UserService()

    user = service.register(name="Alice", email="alice@example.com", password="secret1")

    assert user is not None


def test_register_raises_exception_when_email_missing_at_character():
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Alice", email="alice.example.com", password="secret1")


def test_register_accepts_email_with_at_character():
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    service = UserService()

    user = service.register(name="Alice", email="alice@example.com", password="secret1")

    assert user is not None


def test_register_raises_exception_when_password_has_5_characters():
    # BR03 – The password must have at least 6 characters
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Alice", email="alice@example.com", password="abcde")


def test_register_accepts_password_with_exactly_6_characters():
    # BR03 – The password must have at least 6 characters
    service = UserService()

    user = service.register(name="Alice", email="alice@example.com", password="abcdef")

    assert user is not None


def test_register_raises_exception_when_registering_duplicate_email():
    # BR04 – It is not allowed to register two users with the same email
    # FR03 – The system must prevent registration with a duplicate email
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    service.register(name="Alice", email="dup@example.com", password="secret1")

    with pytest.raises(Exception):
        service.register(name="Bob", email="dup@example.com", password="secret2")


def test_register_allows_registering_different_emails():
    # BR04 – It is not allowed to register two users with the same email
    # FR03 – The system must prevent registration with a duplicate email
    service = UserService()

    user1 = service.register(name="Alice", email="alice1@example.com", password="secret1")
    user2 = service.register(name="Bob", email="alice2@example.com", password="secret2")

    assert user1 is not None
    assert user2 is not None