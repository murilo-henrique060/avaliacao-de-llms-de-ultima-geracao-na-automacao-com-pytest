import pytest

# NOTE:
# These tests assume the production code exposes a `UserService` class with a
# `register(name: str, email: str, password: str) -> User` method, and a `User`
# object with at least `name` and `email` accessible as attributes.
#
# The exact module path is intentionally not specified by the requirements.
# Adjust the import below to match the system under test.
from cases.case01 import UserService  # noqa: F401


def test_fr01_allows_registering_a_user_returns_user_instance():
    # FR01 – The system must allow registering a user
    service = UserService()

    user = service.register(name="Alice", email="alice@example.com", password="secret1")

    assert user is not None


def test_br01_missing_name_raises_exception():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="", email="alice@example.com", password="secret1")


def test_br01_missing_email_raises_exception():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Alice", email="", password="secret1")


def test_br01_missing_password_raises_exception():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Alice", email="alice@example.com", password="")


def test_fr02_validates_email_is_valid_allows_email_with_at_character():
    # FR02 – The system must validate whether the email is valid
    service = UserService()

    user = service.register(name="Bob", email="bob@domain.com", password="secret1")

    assert user is not None


def test_br02_email_without_at_character_raises_exception():
    # BR02 – The email must contain the @ character
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Alice", email="alice.example.com", password="secret1")


def test_br02_email_with_at_character_is_accepted():
    # BR02 – The email must contain the @ character
    service = UserService()

    user = service.register(name="Carol", email="carol@domain.com", password="secret1")

    assert user is not None


def test_br03_password_exactly_6_characters_is_accepted():
    # BR03 – The password must have at least 6 characters
    service = UserService()

    user = service.register(name="Dave", email="dave@example.com", password="123456")

    assert user is not None


def test_br03_password_with_5_characters_raises_exception():
    # BR03 – The password must have at least 6 characters
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Eve", email="eve@example.com", password="12345")


def test_fr03_prevents_registration_with_duplicate_email_raises_exception():
    # FR03 – The system must prevent registration with a duplicate email
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    service.register(name="First", email="dup@example.com", password="secret1")

    with pytest.raises(Exception):
        service.register(name="Second", email="dup@example.com", password="secret2")


def test_br04_registering_two_users_with_same_email_is_not_allowed_raises_exception():
    # BR04 – It is not allowed to register two users with the same email
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    service.register(name="UserA", email="same@example.com", password="secret1")

    with pytest.raises(Exception):
        service.register(name="UserB", email="same@example.com", password="secret1")


def test_fr04_failure_raises_exception_when_email_invalid():
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Frank", email="frankexample.com", password="secret1")