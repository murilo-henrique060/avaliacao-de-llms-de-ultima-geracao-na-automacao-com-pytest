
import pytest

from cases.case01 import UserService, User

# BR01: All users must have a name, email, and password
# FR01: The system must allow registering a user
def test_fr01_register_user_success():
    service = UserService()
    user = service.register("John Doe", "john@example.com", "password123")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

# BR01: All users must have a name, email, and password
# FR04: The system must raise an exception in case of a failure
def test_br01_missing_name_failure():
    service = UserService()
    with pytest.raises(Exception):
        service.register("", "john@example.com", "password123")

# BR01: All users must have a name, email, and password
# FR04: The system must raise an exception in case of a failure
def test_br01_missing_email_failure():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "", "password123")

# BR01: All users must have a name, email, and password
# FR04: The system must raise an exception in case of a failure
def test_br01_missing_password_failure():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "john@example.com", "")

# BR02: The email must contain the @ character
# FR02: The system must validate whether the email is valid
def test_br02_email_with_at_character_success():
    service = UserService()
    user = service.register("John Doe", "john@example.com", "password123")
    assert "@" in user.email

# BR02: The email must contain the @ character
# FR02: The system must validate whether the email is valid
# FR04: The system must raise an exception in case of a failure
def test_br02_email_without_at_character_failure():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "john.example.com", "password123")

# BR03: The password must have at least 6 characters
def test_br03_password_with_exactly_six_characters_success():
    service = UserService()
    user = service.register("John Doe", "john@example.com", "123456")
    assert user.name == "John Doe"

# BR03: The password must have at least 6 characters
# FR04: The system must raise an exception in case of a failure
def test_br03_password_with_five_characters_failure():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "john@example.com", "12345")

# BR04: It is not allowed to register two users with the same email
# FR03: The system must prevent registration with a duplicate email
# FR04: The system must raise an exception in case of a failure
def test_br04_duplicate_email_registration_failure():
    service = UserService()
    service.register("User One", "duplicate@example.com", "password123")
    with pytest.raises(Exception):
        service.register("User Two", "duplicate@example.com", "password456")
