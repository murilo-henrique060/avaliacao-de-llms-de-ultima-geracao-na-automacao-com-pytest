
import pytest

from cases.case01 import UserService, User

# Assuming classes User and UserService are defined in the system according to the Class Diagram.
# Classes are not implemented here as per instruction "Do not implement the system — tests only."

def test_fr01_br01_register_user_successfully():
    # FR01 – The system must allow registering a user
    # BR01 – All users must have a name, email, and password
    service = UserService()
    user = service.register("John Doe", "john@example.com", "password123")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    assert isinstance(user, User)

def test_br01_registration_fails_without_name():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    with pytest.raises(Exception):
        service.register(None, "john@example.com", "password123")

def test_br01_registration_fails_without_email():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", None, "password123")

def test_br01_registration_fails_without_password():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    with pytest.raises(Exception):
        service.register("John Doe", "john@example.com", None)

def test_br02_fr02_email_contains_at_character_success():
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    service = UserService()
    user = service.register("Jane Doe", "jane@example.com", "password123")
    assert "@" in user.email

def test_br02_fr02_email_without_at_character_fails():
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    with pytest.raises(Exception):
        service.register("Jane Doe", "jane-at-example.com", "password123")

def test_br03_password_minimum_length_edge_case_6_characters():
    # BR03 – The password must have at least 6 characters
    service = UserService()
    user = service.register("Bob Smith", "bob@example.com", "123456")
    assert isinstance(user, User)

def test_br03_password_below_minimum_length_fails():
    # BR03 – The password must have at least 6 characters
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    with pytest.raises(Exception):
        service.register("Bob Smith", "bob@example.com", "12345")

def test_br04_fr03_prevent_duplicate_email_registration():
    # BR04 – It is not allowed to register two users with the same email
    # FR03 – The system must prevent registration with a duplicate email
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    service.register("First User", "unique@example.com", "password123")
    with pytest.raises(Exception):
        service.register("Second User", "unique@example.com", "password456")
