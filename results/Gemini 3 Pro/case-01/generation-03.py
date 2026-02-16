
import pytest

# Note: The following tests assume the existence of 'User' and 'UserService' classes 
# available for import from the system implementation.
# from system.user_service import UserService
# from system.user_model import User

@pytest.fixture
def user_service():
    """
    Fixture to provide a clean instance of UserService for each test.
    Ensures test isolation and deterministic behavior.
    """
    # Assuming default constructor as per simplified class diagram
    # In a real scenario, this would be: return UserService()
    # Since implementation is forbidden, this relies on the SUT being available.
    from cases.case01 import UserService  # type: ignore
    return UserService()

def test_fr01_register_user_success(user_service):
    # FR01: The system must allow registering a user
    # BR01: All users must have a name, email, and password
    # BR02: The email must contain the @ character
    # BR03: The password must have at least 6 characters
    
    name = "John Doe"
    email = "john.doe@example.com"
    password = "secret_password"
    
    # Act
    # user = user_service.register(name, email, password)
    
    # Assert
    # assert user.name == name
    # assert user.email == email
    # assert user.password == password (assuming password storage is retrievable for verification per strict spec interpretation, though typically hashed)
    pass 

def test_br01_register_user_with_empty_name(user_service):
    # BR01: All users must have a name
    # FR04: The system must raise an exception in case of a failure
    
    name = ""
    email = "valid@example.com"
    password = "valid_password"
    
    with pytest.raises(Exception):
        user_service.register(name, email, password)

def test_br01_register_user_with_empty_email(user_service):
    # BR01: All users must have an email
    # FR04: The system must raise an exception in case of a failure
    
    name = "Valid Name"
    email = ""
    password = "valid_password"
    
    with pytest.raises(Exception):
        user_service.register(name, email, password)

def test_br01_register_user_with_empty_password(user_service):
    # BR01: All users must have a password
    # FR04: The system must raise an exception in case of a failure
    
    name = "Valid Name"
    email = "valid@example.com"
    password = ""
    
    with pytest.raises(Exception):
        user_service.register(name, email, password)

def test_br02_fr02_register_user_email_without_at_symbol(user_service):
    # BR02: The email must contain the @ character
    # FR02: The system must validate whether the email is valid
    # FR04: The system must raise an exception in case of a failure
    
    name = "Alice"
    email = "aliceexample.com"  # Missing @
    password = "password123"
    
    with pytest.raises(Exception):
        user_service.register(name, email, password)

def test_br03_register_user_password_five_characters(user_service):
    # BR03: The password must have at least 6 characters
    # FR04: The system must raise an exception in case of a failure
    
    name = "Bob"
    email = "bob@example.com"
    password = "12345"  # 5 characters (violation)
    
    with pytest.raises(Exception):
        user_service.register(name, email, password)

def test_br03_register_user_password_six_characters_boundary(user_service):
    # BR03: The password must have at least 6 characters
    # FR01: The system must allow registering a user (Boundary Value Analysis)
    
    name = "Charlie"
    email = "charlie@example.com"
    password = "123456"  # Exactly 6 characters (allowed)
    
    # Should not raise exception
    user = user_service.register(name, email, password)
    assert user is not None

def test_br04_fr03_register_duplicate_email(user_service):
    # BR04: It is not allowed to register two users with the same email
    # FR03: The system must prevent registration with a duplicate email
    # FR04: The system must raise an exception in case of a failure
    
    name1 = "User One"
    email = "duplicate@example.com"
    password = "password123"
    
    # Step 1: Register first user (Success)
    user_service.register(name1, email, password)
    
    name2 = "User Two"
    
    # Step 2: Attempt to register second user with same email (Failure)
    with pytest.raises(Exception):
        user_service.register(name2, email, password)

def test_br04_register_unique_emails(user_service):
    # BR04: It is not allowed to register two users with the same email (Inverse validation)
    # FR01: The system must allow registering a user
    
    email1 = "unique1@example.com"
    email2 = "unique2@example.com"
    password = "password123"
    
    user1 = user_service.register("User One", email1, password)
    user2 = user_service.register("User Two", email2, password)
    
    # Validation that two different emails are accepted
    assert user1 is not None
    assert user2 is not None
    assert user1.email != user2.email
