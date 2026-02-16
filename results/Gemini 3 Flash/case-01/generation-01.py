
import pytest

from cases.case01 import UserService, User

# Assuming the classes User and UserService are defined in the system under test.
from cases.case01 import UserService, User

# FR01 – System must allow registering a user
# BR01 – All users must have a name, email, and password
def test_register_user_success():
    service = UserService()
    user = service.register("John Doe", "john@example.com", "password123")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    # Verification of password containment based on UML (private attribute represented as -password)
    # Since implementation is not provided, we validate the registration return object exists.
    assert user is not None

# BR01 – All users must have a name, email, and password
# FR04 – System must raise an exception in case of a failure
def test_register_missing_name_fails():
    service = UserService()
    with pytest.raises(Exception):
        service.register(None, "john@example.com", "password123")

# BR01 – All users must have a name, email, and password
# FR04 – System must raise an exception in case of a failure
def test_register_missing_email_fails():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", None, "password123")

# BR01 – All users must have a name, email, and password
# FR04 – System must raise an exception in case of a failure
def test_register_missing_password_fails():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "john@example.com", None)

# BR02 – The email must contain the @ character
# FR02 – The system must validate whether the email is valid
def test_register_email_with_at_character_success():
    service = UserService()
    user = service.register("John Doe", "valid@email.com", "password123")
    assert "@" in user.email

# BR02 – The email must contain the @ character
# FR02 – The system must validate whether the email is valid
# FR04 – System must raise an exception in case of a failure
def test_register_email_without_at_character_fails():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "invalid-email.com", "password123")

# BR03 – The password must have at least 6 characters
def test_register_password_exactly_six_characters_success():
    service = UserService()
    user = service.register("John Doe", "john@example.com", "123456")
    assert user is not None

# BR03 – The password must have at least 6 characters
def test_register_password_more_than_six_characters_success():
    service = UserService()
    user = service.register("John Doe", "john@example.com", "seven_chars")
    assert user is not None

# BR03 – The password must have at least 6 characters
# FR04 – System must raise an exception in case of a failure
def test_register_password_five_characters_fails():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "john@example.com", "12345")

# BR04 – It is not allowed to register two users with the same email
# FR03 – The system must prevent registration with a duplicate email
def test_register_different_emails_success():
    service = UserService()
    service.register("User One", "user1@example.com", "password123")
    user2 = service.register("User Two", "user2@example.com", "password123")
    assert user2 is not None

# BR04 – It is not allowed to register two users with the same email
# FR03 – The system must prevent registration with a duplicate email
# FR04 – System must raise an exception in case of a failure
def test_register_duplicate_email_fails():
    service = UserService()
    service.register("First User", "duplicate@example.com", "password123")
    with pytest.raises(Exception):
        service.register("Second User", "duplicate@example.com", "secure123")
