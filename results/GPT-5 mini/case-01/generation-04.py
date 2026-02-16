import pytest
from cases.case01 import UserService, User

# BR01 – All users must have a name, email, and password
def test_br01_register_with_all_fields_returns_user_instance():
    service = UserService()
    user = service.register(name="Alice", email="alice@example.com", password="secure1")
    assert isinstance(user, User)

# BR01 – All users must have a name, email, and password
def test_br01_missing_name_raises_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="", email="no-name@example.com", password="secure1")

# BR01 – All users must have a name, email, and password
def test_br01_missing_email_raises_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="NoEmail", email="", password="secure1")

# BR01 – All users must have a name, email, and password
def test_br01_missing_password_raises_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="NoPassword", email="nopass@example.com", password="")

# BR02 – The email must contain the @ character
def test_br02_valid_email_with_at_succeeds():
    service = UserService()
    user = service.register(name="Bob", email="bob@domain.com", password="abcdef")
    assert isinstance(user, User)

# BR02 – The email must contain the @ character
def test_br02_email_without_at_raises_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="Eve", email="eve.domain.com", password="abcdef")

# BR03 – The password must have at least 6 characters
def test_br03_password_with_exact_six_characters_succeeds():
    service = UserService()
    user = service.register(name="Carol", email="carol@example.com", password="123456")
    assert isinstance(user, User)

# BR03 – The password must have at least 6 characters
def test_br03_password_with_five_characters_raises_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="Dave", email="dave@example.com", password="12345")

# BR04 – It is not allowed to register two users with the same email
def test_br04_register_two_different_emails_succeeds_for_both():
    service = UserService()
    user1 = service.register(name="User1", email="u1@example.com", password="password1")
    user2 = service.register(name="User2", email="u2@example.com", password="password2")
    assert isinstance(user1, User) and isinstance(user2, User)

# BR04 – It is not allowed to register two users with the same email
def test_br04_register_duplicate_email_raises_exception_on_second_registration():
    service = UserService()
    service.register(name="Original", email="dup@example.com", password="original")
    with pytest.raises(Exception):
        service.register(name="Duplicate", email="dup@example.com", password="duplicate")

# FR01 – The system must allow registering a user
def test_fr01_register_returns_user_object_on_success():
    service = UserService()
    user = service.register(name="Frank", email="frank@example.com", password="frankpw")
    assert isinstance(user, User)

# FR02 – The system must validate whether the email is valid
def test_fr02_invalid_email_triggers_validation_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="Grace", email="graceexample.com", password="gracepw")

# FR03 – The system must prevent registration with a duplicate email
def test_fr03_duplicate_email_prevention_raises_exception():
    service = UserService()
    service.register(name="Hank", email="hank@example.com", password="hankpw")
    with pytest.raises(Exception):
        service.register(name="Hank2", email="hank@example.com", password="hankpw2")

# FR04 – The system must raise an exception in case of a failure
def test_fr04_failures_raise_exceptions_using_pytest_raises():
    service = UserService()
    with pytest.raises(Exception):
        # Trigger a failure (invalid email) and assert that an exception is raised
        service.register(name="Ivy", email="ivyexample.com", password="ivypw")