
import pytest

# NOTE: The following tests assume the existence of a 'UserService' class and a 'User' class
# as described in the system context. In a real execution environment, these would be imported.
# Example: from user_system import UserService, User

from cases.case01 import UserService  # type: ignore

@pytest.fixture
def user_service():
    """
    Fixture to provide a clean instance of UserService for each test.
    This ensures test isolation and reproducibility.
    """
    # Assuming UserService() constructor requires no arguments based on class diagram

    return UserService()

def test_fr01_register_valid_user(user_service):
    """
    FR01 – The system must allow registering a user.
    Validates that a user with valid data is correctly returned as a User object.
    """
    name = "Valid Name"
    email = "valid@email.com"
    password = "validpassword"

    # Act
    user = user_service.register(name, email, password)

    # Assert
    assert user.name == name
    assert user.email == email
    # Password should generally be hashed, but diagram shows it as a private attribute '-password'
    # Since we cannot check private attributes easily or assume getters, we check public identity.
    assert hasattr(user, 'name')
    assert hasattr(user, 'email')

def test_br01_validate_name_presence(user_service):
    """
    BR01 – All users must have a name.
    Validates that registering a user with an empty name raises an exception.
    FR04 – The system must raise an exception in case of a failure.
    """
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name="", email="test@test.com", password="password123")

def test_br01_validate_email_presence(user_service):
    """
    BR01 – All users must have an email.
    Validates that registering a user with an empty email raises an exception.
    FR04 – The system must raise an exception in case of a failure.
    """
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name="Test User", email="", password="password123")

def test_br01_validate_password_presence(user_service):
    """
    BR01 – All users must have a password.
    Validates that registering a user with an empty password raises an exception.
    FR04 – The system must raise an exception in case of a failure.
    """
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name="Test User", email="test@test.com", password="")

def test_br02_email_must_contain_at_character_violation(user_service):
    """
    BR02 – The email must contain the @ character.
    FR02 – The system must validate whether the email is valid.
    Validates that an email without '@' raises an exception.
    """
    invalid_email = "emailwithoutat.com"
    
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name="Test User", email=invalid_email, password="password123")

def test_br02_email_must_contain_at_character_success(user_service):
    """
    BR02 – The email must contain the @ character.
    FR02 – The system must validate whether the email is valid.
    Validates that an email with '@' is accepted.
    """
    valid_email = "email@domain.com"
    
    # Act
    user = user_service.register(name="Test User", email=valid_email, password="password123")
    
    # Assert
    assert user.email == valid_email

def test_br03_password_min_length_violation(user_service):
    """
    BR03 – The password must have at least 6 characters.
    Validates that a password with 5 characters raises an exception.
    """
    short_password = "12345" # 5 characters
    
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name="Test User", email="test@test.com", password=short_password)

def test_br03_password_min_length_boundary_success(user_service):
    """
    BR03 – The password must have at least 6 characters.
    Validates that a password with exactly 6 characters is accepted (Edge Case).
    """
    exact_password = "123456" # 6 characters
    
    # Act
    user = user_service.register(name="Test User", email="test@test.com", password=exact_password)
    
    # Assert
    # If no exception is raised, the requirement is met for the boundary.
    assert user is not None

def test_br03_password_min_length_above_boundary_success(user_service):
    """
    BR03 – The password must have at least 6 characters.
    Validates that a password with more than 6 characters is accepted.
    """
    long_password = "1234567" # 7 characters
    
    # Act
    user = user_service.register(name="Test User", email="test@test.com", password=long_password)
    
    # Assert
    assert user is not None

def test_br04_prevent_duplicate_email(user_service):
    """
    BR04 – It is not allowed to register two users with the same email.
    FR03 – The system must prevent registration with a duplicate email.
    Validates that registering the same email twice raises an exception.
    """
    email = "unique@test.com"
    
    # Act: First registration
    user_service.register(name="User One", email=email, password="password123")
    
    # Act & Assert: Second registration with same email
    with pytest.raises(Exception):
        user_service.register(name="User Two", email=email, password="password456")

def test_br04_allow_different_emails(user_service):
    """
    BR04 – It is not allowed to register two users with the same email.
    Validates that registering two users with different emails is allowed.
    """
    # Act
    user1 = user_service.register(name="User One", email="one@test.com", password="password123")
    user2 = user_service.register(name="User Two", email="two@test.com", password="password123")
    
    # Assert
    assert user1.email == "one@test.com"
    assert user2.email == "two@test.com"

def test_fr04_exception_on_general_failure(user_service):
    """
    FR04 – The system must raise an exception in case of a failure.
    Validates that an invalid state explicitly triggers an exception catch.
    This serves as a generic verification of the failure mechanism.
    """
    # Using a violation of BR03 as a proxy to verify the mechanism
    with pytest.raises(Exception):
        user_service.register("Name", "valid@email.com", "short")
