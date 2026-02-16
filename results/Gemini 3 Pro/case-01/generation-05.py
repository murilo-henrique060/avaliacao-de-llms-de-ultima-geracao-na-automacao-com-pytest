
import pytest
from unittest.mock import MagicMock

# --- ASSUMED IMPORTS ---
# Based on the prompt's constraints ("Do not implement the system"),
# we assume the following classes exist in the module 'user_registration_system'.
# For the purpose of making these tests syntactically valid and runnable in a mock environment,
# we will mock the dependencies if the module is not found, or strict imports if required.
# However, to strictly adhere to "Generate tests only", we assume imports work.

try:
    from cases.case01 import UserService, User
except ImportError:
    # This block allows the tests to be parsed/run in an environment without the implementation,
    # effectively satisfying the requirement to generate valid Python code that *would* run.
    # In a real pipeline, the system module would be present.
    pass

# --- FIXTURES ---

@pytest.fixture
def user_service():
    """
    Fixture to provide a fresh instance of UserService for each test.
    Ensures state isolation between tests.
    """
    return UserService()

# --- TESTS FOR BUSINESS RULES (BR) ---

def test_register_user_success(user_service):
    """
    FR01 - The system must allow registering a user.
    BR01 - All users must have a name, email, and password.
    
    Validates that a user with valid data is correctly registered and returned.
    """
    # Arrange
    name = "John Doe"
    email = "john.doe@example.com"
    password = "securePassword123"

    # Act
    user = user_service.register(name, email, password)

    # Assert
    assert user is not None
    assert user.name == name
    assert user.email == email
    # Password should typically be hashed, but verifying the object creation for now.

def test_register_user_missing_name_raises_exception(user_service):
    """
    BR01 - All users must have a name, email, and password.
    FR04 - The system must raise an exception in case of a failure.
    
    Validates that registering a user with an empty name raises an exception.
    """
    # Arrange
    name = ""
    email = "valid@example.com"
    password = "validPassword"

    # Act & Assert
    with pytest.raises(ValueError):
        user_service.register(name, email, password)

def test_register_user_missing_email_raises_exception(user_service):
    """
    BR01 - All users must have a name, email, and password.
    FR04 - The system must raise an exception in case of a failure.
    
    Validates that registering a user with an empty email raises an exception.
    """
    # Arrange
    name = "Valid Name"
    email = ""
    password = "validPassword"

    # Act & Assert
    with pytest.raises(ValueError):
        user_service.register(name, email, password)

def test_register_user_missing_password_raises_exception(user_service):
    """
    BR01 - All users must have a name, email, and password.
    FR04 - The system must raise an exception in case of a failure.
    
    Validates that registering a user with an empty password raises an exception.
    """
    # Arrange
    name = "Valid Name"
    email = "valid@example.com"
    password = ""

    # Act & Assert
    with pytest.raises(ValueError):
        user_service.register(name, email, password)

def test_register_user_email_without_at_sign_raises_exception(user_service):
    """
    BR02 - The email must contain the @ character.
    FR02 - The system must validate whether the email is valid.
    FR04 - The system must raise an exception in case of a failure.
    
    Validates that an email missing the '@' symbol causes an exception.
    """
    # Arrange
    name = "John Doe"
    email = "johndoe.com"  # Invalid email
    password = "validPassword"

    # Act & Assert
    with pytest.raises(ValueError):
        user_service.register(name, email, password)

def test_register_user_password_too_short_raises_exception(user_service):
    """
    BR03 - The password must have at least 6 characters.
    FR04 - The system must raise an exception in case of a failure.
    
    Validates that a password with 5 characters (below limit) raises an exception.
    """
    # Arrange
    name = "John Doe"
    email = "john@example.com"
    password = "12345"  # 5 chars

    # Act & Assert
    with pytest.raises(ValueError):
        user_service.register(name, email, password)

def test_register_user_password_exact_min_length_success(user_service):
    """
    BR03 - The password must have at least 6 characters.
    FR01 - The system must allow registering a user.
    
    Edge Case: Validates that a password with exactly 6 characters is accepted.
    """
    # Arrange
    name = "John Doe"
    email = "john@example.com"
    password = "123456"  # Exactly 6 chars

    # Act
    user = user_service.register(name, email, password)

    # Assert
    assert user is not None

def test_register_duplicate_email_raises_exception(user_service):
    """
    BR04 - It is not allowed to register two users with the same email.
    FR03 - The system must prevent registration with a duplicate email.
    FR04 - The system must raise an exception in case of a failure.
    
    Validates that registering a second user with an existing email raises an exception.
    """
    # Arrange
    name1 = "User One"
    email = "duplicate@example.com"
    password = "password123"
    
    name2 = "User Two"
    # Same email, different name/password to isolate the email cause

    # Act
    user_service.register(name1, email, password)

    # Assert
    with pytest.raises(Exception): # Using generic Exception as specific type is not defined in specs
        user_service.register(name2, email, password)
