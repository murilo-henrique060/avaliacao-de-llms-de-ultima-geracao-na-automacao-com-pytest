
import pytest

from cases.case01 import UserService, User


# As per the task instructions, only tests are generated. 
# The UserService and User classes are assumed to exist according to the Class Diagram.

def test_fr01_br01_successful_user_registration():
    # FR01 – The system must allow registering a user
    # BR01 – All users must have a name, email, and password
    service = UserService()
    user = service.register(name="John Doe", email="john@example.com", password="securepassword")
    
    assert user.name == "John Doe"
    assert user.email == "john@example.com"
    # Password is private in the diagram (- password), but register must accept it.

def test_br01_fr04_registration_without_name_fails():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="", email="john@example.com", password="password123")

def test_br01_fr04_registration_without_email_fails():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="John Doe", email="", password="password123")

def test_br01_fr04_registration_without_password_fails():
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="John Doe", email="john@example.com", password="")

def test_br02_fr02_email_validation_contains_at_character():
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    service = UserService()
    # Positive case: contains '@'
    user = service.register(name="Jane Doe", email="jane@example.com", password="password123")
    assert "@" in user.email

def test_br02_fr02_fr04_email_without_at_character_fails():
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    with pytest.raises(Exception):
        service.register(name="Jane Doe", email="jane-at-example.com", password="password123")

def test_br03_password_minimum_length_boundary_six_chars():
    # BR03 – The password must have at least 6 characters
    service = UserService()
    # Edge case: Exactly 6 characters should be valid
    user = service.register(name="User Six", email="six@example.com", password="123456")
    assert user is not None

def test_br03_fr04_password_less_than_six_characters_fails():
    # BR03 – The password must have at least 6 characters
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    # Negative case: 5 characters
    with pytest.raises(Exception):
        service.register(name="User Five", email="five@example.com", password="12345")

def test_br04_fr03_fr04_prevent_duplicate_email_registration():
    # BR04 – It is not allowed to register two users with the same email
    # FR03 – The system must prevent registration with a duplicate email
    # FR04 – The system must raise an exception in case of a failure
    service = UserService()
    email = "duplicate@example.com"
    
    # First registration
    service.register(name="First User", email=email, password="password123")
    
    # Second registration with same email
    with pytest.raises(Exception):
        service.register(name="Second User", email=email, password="differentpassword")
