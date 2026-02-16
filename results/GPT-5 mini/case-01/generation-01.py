import pytest
from cases.case01 import UserService, User

# BR01 – All users must have a name, email, and password
def test_br01_register_user_with_all_fields_succeeds():
    service = UserService()
    user = service.register("Alice", "alice@example.com", "password123")
    # Validate that registration succeeded by checking the returned user's email
    assert user.email == "alice@example.com"

# BR01 – All users must have a name, email, and password
def test_br01_register_without_name_raises_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register(None, "bob@example.com", "password123")

# BR02 – Email must contain the @ character
def test_br02_email_with_at_allows_registration():
    service = UserService()
    user = service.register("Carol", "carol@example.com", "passw0rd")
    # Validate registration succeeded for an email containing '@'
    assert user.email == "carol@example.com"

# BR02 – Email must contain the @ character
def test_br02_email_missing_at_raises_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register("Dave", "dave.example.com", "password123")

# BR03 – The password must have at least 6 characters
def test_br03_password_exactly_six_characters_is_accepted():
    service = UserService()
    user = service.register("Eve", "eve@example.com", "123456")
    # Validate registration succeeded when password has exactly 6 characters
    assert user.email == "eve@example.com"

# BR03 – The password must have at least 6 characters
def test_br03_password_five_characters_raises_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register("Frank", "frank@example.com", "12345")

# BR04 – It is not allowed to register two users with the same email.
def test_br04_registering_two_users_with_same_email_raises_exception_on_second():
    service = UserService()
    service.register("Gina", "gina@example.com", "password123")
    with pytest.raises(Exception):
        service.register("Hank", "gina@example.com", "anotherpass")

# BR04 – It is not allowed to register two users with the same email.
def test_br04_registering_two_different_emails_succeeds_for_both():
    service = UserService()
    service.register("Ivy", "ivy@example.com", "password123")
    user2 = service.register("Jack", "jack@example.com", "password123")
    # Validate second registration with a different email succeeds
    assert user2.email == "jack@example.com"

# FR01 – The system must allow registering a user
def test_fr01_register_returns_user_instance():
    service = UserService()
    user = service.register("Kate", "kate@example.com", "pass123")
    # Validate that a User instance is returned upon successful registration
    assert isinstance(user, User)

# FR02 – The system must validate whether the email is valid
def test_fr02_invalid_email_causes_validation_exception():
    service = UserService()
    with pytest.raises(Exception):
        service.register("Leo", "leoexample.com", "password123")

# FR03 – The system must prevent registration with a duplicate email
def test_fr03_prevent_registration_with_duplicate_email():
    service = UserService()
    service.register("Mia", "mia@example.com", "password123")
    with pytest.raises(Exception):
        service.register("Ned", "mia@example.com", "password456")

# FR04 – The system must raise an exception in case of a failure
def test_fr04_system_raises_exception_on_validation_failure():
    service = UserService()
    with pytest.raises(Exception):
        service.register(None, "oliver@example.com", "pass123")