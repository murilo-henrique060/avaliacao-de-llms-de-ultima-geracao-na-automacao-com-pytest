
import pytest

from cases.case01 import UserService, User


# Since the task is to generate tests only without implementing the system, 
# it is assumed that User and UserService are available in the environment 
# or imported from the system module.

# FR01 – The system must allow registering a user
def test_register_user_functional_requirement_fulfillment():
    service = UserService()
    user = service.register("John Doe", "john@example.com", "password123")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

# BR01 – All users must have a name
# FR04 – The system must raise an exception in case of a failure
def test_registration_fails_when_name_is_missing():
    service = UserService()
    with pytest.raises(Exception):
        service.register(None, "john@example.com", "password123")

# BR01 – All users must have an email
# FR04 – The system must raise an exception in case of a failure
def test_registration_fails_when_email_is_missing():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", None, "password123")

# BR01 – All users must have a password
# FR04 – The system must raise an exception in case of a failure
def test_registration_fails_when_password_is_missing():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "john@example.com", None)

# BR02 – The email must contain the @ character
# FR02 – The system must validate whether the email is valid
def test_registration_accepts_email_with_at_character():
    service = UserService()
    user = service.register("John Doe", "valid@email.com", "password123")
    assert "@" in user.email

# BR02 – The email must contain the @ character
# FR02 – The system must validate whether the email is valid
# FR04 – The system must raise an exception in case of a failure
def test_registration_fails_when_email_lacks_at_character():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "invalid.email.com", "password123")

# BR03 – The password must have at least 6 characters
def test_registration_accepts_password_with_exactly_six_characters():
    service = UserService()
    user = service.register("John Doe", "john@example.com", "123456")
    # No exception raised, user created successfully
    assert user is not None

# BR03 – The password must have at least 6 characters
# FR04 – The system must raise an exception in case of a failure
def test_registration_fails_when_password_has_five_characters():
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "john@example.com", "12345")

# BR04 – It is not allowed to register two users with the same email
# FR03 – The system must prevent registration with a duplicate email
def test_registration_allows_different_emails():
    service = UserService()
    service.register("User One", "user1@example.com", "password123")
    user2 = service.register("User Two", "user2@example.com", "password123")
    assert user2.email == "user2@example.com"

# BR04 – It is not allowed to register two users with the same email
# FR03 – The system must prevent registration with a duplicate email
# FR04 – The system must raise an exception in case of a failure
def test_registration_fails_with_duplicate_email():
    service = UserService()
    service.register("First User", "duplicate@example.com", "password123")
    with pytest.raises(Exception):
        service.register("Second User", "duplicate@example.com", "otherpassword")
