import pytest

# which provides `UserService` and `User` as described in the specification.
from cases.case01 import UserService, User


# BR01 – All users must have a name, email, and password
def test_br01_register_with_all_fields_succeeds_returns_user():
    service = UserService()
    # Validate only BR01: registration with all required fields returns a User
    user = service.register(name="Alice", email="alice@example.com", password="securepw")
    assert isinstance(user, User)


# BR01 – All users must have a name, email, and password
def test_br01_missing_name_raises_exception():
    service = UserService()
    # Missing name (None) must cause a validation failure (exception)
    with pytest.raises(Exception):
        service.register(name=None, email="bob@example.com", password="securepw")


# BR01 – All users must have a name, email, and password
def test_br01_missing_email_raises_exception():
    service = UserService()
    # Missing email (None) must cause a validation failure (exception)
    with pytest.raises(Exception):
        service.register(name="Bob", email=None, password="securepw")


# BR01 – All users must have a name, email, and password
def test_br01_missing_password_raises_exception():
    service = UserService()
    # Missing password (None) must cause a validation failure (exception)
    with pytest.raises(Exception):
        service.register(name="Carol", email="carol@example.com", password=None)


# BR02 – Email must contain the @ character
def test_br02_email_with_at_is_accepted():
    service = UserService()
    # Validate only BR02: an email containing '@' must be accepted (registration succeeds)
    user = service.register(name="Dave", email="dave@domain.com", password="strongpwd")
    assert isinstance(user, User)


# BR02 – Email must contain the @ character
def test_br02_email_without_at_raises_exception():
    service = UserService()
    # Email missing '@' must cause a validation failure (exception)
    with pytest.raises(Exception):
        service.register(name="Eve", email="evedomain.com", password="strongpwd")


# BR03 – The password must have at least 6 characters
def test_br03_password_exactly_six_characters_is_accepted():
    service = UserService()
    # Edge case: password length exactly 6 must be accepted
    user = service.register(name="Frank", email="frank@example.com", password="ABCDEF")
    assert isinstance(user, User)


# BR03 – The password must have at least 6 characters
def test_br03_password_five_characters_raises_exception():
    service = UserService()
    # Password of length 5 must cause a validation failure (exception)
    with pytest.raises(Exception):
        service.register(name="Grace", email="grace@example.com", password="ABCDE")


# BR04 – It is not allowed to register two users with the same email
def test_br04_registering_duplicate_email_raises_exception_on_second_registration():
    service = UserService()
    # First registration with the email is setup (no assertion here; it's setup only)
    service.register(name="Heidi", email="dup@example.com", password="password1")
    # Second registration with the same email must raise an exception
    with pytest.raises(Exception):
        service.register(name="Heidi2", email="dup@example.com", password="password2")


# FR01 – The system must allow registering a user
def test_fr01_valid_registration_returns_user():
    service = UserService()
    # Validate FR01: a valid registration must return a User object
    user = service.register(name="Ivan", email="ivan@example.com", password="validpw")
    assert isinstance(user, User)


# FR02 – The system must validate whether the email is valid
def test_fr02_invalid_email_registration_raises_exception():
    service = UserService()
    # Validate FR02: invalid email must cause the system to raise an exception
    with pytest.raises(Exception):
        service.register(name="Judy", email="judydomain.com", password="validpw")


# FR03 – The system must prevent registration with a duplicate email
def test_fr03_duplicate_email_prevention_raises_exception():
    service = UserService()
    # Setup: register first user (no assertion to keep test focused on FR03)
    service.register(name="Karl", email="karl@example.com", password="pwd12345")
    # Validate FR03: attempt to register another user with the same email must raise
    with pytest.raises(Exception):
        service.register(name="Karl2", email="karl@example.com", password="pwd54321")


# FR04 – The system must raise an exception in case of a failure
def test_fr04_failure_conditions_raise_exception():
    service = UserService()
    # Trigger a failure condition (invalid email) and assert an exception is raised per FR04
    with pytest.raises(Exception):
        service.register(name="Laura", email="lauradomain.com", password="validpw")