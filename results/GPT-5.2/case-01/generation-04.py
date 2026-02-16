import pytest

# NOTE:
# These tests assume the SUT provides a UserService class with:
#   register(name: str, email: str, password: str) -> User
# and a User object with public attributes: name, email.
# Password is private in the UML (- password: str), so tests do not access it directly.

from cases.case01 import UserService  # type: ignore


def test_register_returns_user_instance_when_all_fields_valid():
    # FR01 – The system must allow registering a user
    service = UserService()

    user = service.register(name="Alice", email="alice@example.com", password="secret1")

    assert user is not None


def test_register_raises_exception_when_name_is_missing():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="", email="alice@example.com", password="secret1")


def test_register_raises_exception_when_email_is_missing():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Alice", email="", password="secret1")


def test_register_raises_exception_when_password_is_missing():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Alice", email="alice@example.com", password="")


def test_register_accepts_email_containing_at_character():
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    service = UserService()

    user = service.register(name="Bob", email="bob@example.com", password="secret1")

    assert user.email == "bob@example.com"


def test_register_raises_exception_when_email_missing_at_character():
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Bob", email="bobexample.com", password="secret1")


def test_register_accepts_password_with_exactly_6_characters():
    # BR03 – The password must have at least 6 characters
    service = UserService()

    user = service.register(name="Carol", email="carol@example.com", password="123456")

    assert user.email == "carol@example.com"


def test_register_raises_exception_when_password_has_5_characters():
    # BR03 – The password must have at least 6 characters
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    with pytest.raises(Exception):
        service.register(name="Carol", email="carol@example.com", password="12345")


def test_register_prevents_duplicate_email_by_raising_exception():
    # BR04 – It is not allowed to register two users with the same email
    # FR03 – The system must prevent registration with a duplicate email
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()

    service.register(name="Dave", email="dup@example.com", password="secret1")

    with pytest.raises(Exception):
        service.register(name="Eve", email="dup@example.com", password="secret2")