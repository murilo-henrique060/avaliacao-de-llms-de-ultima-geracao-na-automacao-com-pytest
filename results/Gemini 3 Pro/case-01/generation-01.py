
import pytest
from unittest.mock import Mock, MagicMock

# Assumptions for the test execution context:
# 1. The classes User and UserService are imported from the system module.
# 2. Since the implementation is not provided, we assume the existence of these classes
#    for the tests to be syntactically valid.
# 3. We assume the UserService maintains state for the duration of the test instance 
#    to validate BR04 (Duplicate emails).

# Mocking the SUT (System Under Test) strictly for the purpose of test structure validity
# in a real scenario, these would be imported: "from system import UserService, User"

class User:
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

class UserService:
    def __init__(self):
        self.users = []

    def register(self, name, email, password):
        # Implementation is stubbed to allow tests to run if strictly needed,
        # but logic relies on the tests defining expectations.
        pass

@pytest.fixture
def user_service():
    """
    Fixture to provide a clean instance of UserService for each test.
    Ensures tests are deterministic and isolated.
    """
    from cases.case01 import UserService  # type: ignore
    return UserService()

# -------------------------------------------------------------------------
# FR01 – The system must allow registering a user
# BR01 – All users must have a name, email, and password
# -------------------------------------------------------------------------

def test_register_user_success(user_service):
    # FR01 – The system must allow registering a user
    # BR01 – All users must have a name, email, and password
    
    # Arrange
    name = "John Doe"
    email = "john.doe@example.com"
    password = "securepassword"
    
    # Act
    # We assume the real implementation returns a User object
    # For a real run, we would mock user_service.register to return a User
    # but strictly following the prompt, we write the test invocation.
    result = user_service.register(name, email, password)
    
    # Assert
    # Validates that a User object is returned with correct data
    # Note: In a real TDD cycle, assertions would depend on return type implementation details.
    assert result is not None
    assert result.name == "John Doe"
    assert result.email == "john.doe@example.com"

# -------------------------------------------------------------------------
# BR01 – All users must have a name, email, and password
# FR04 – The system must raise an exception in case of a failure
# -------------------------------------------------------------------------

def test_register_user_missing_name_raises_exception(user_service):
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    
    # Arrange
    name = ""
    email = "valid@example.com"
    password = "password123"
    
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name, email, password)

def test_register_user_missing_email_raises_exception(user_service):
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    
    # Arrange
    name = "Valid Name"
    email = ""
    password = "password123"
    
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name, email, password)

def test_register_user_missing_password_raises_exception(user_service):
    # BR01 – All users must have a name, email, and password
    # FR04 – The system must raise an exception in case of a failure
    
    # Arrange
    name = "Valid Name"
    email = "valid@example.com"
    password = ""
    
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name, email, password)

# -------------------------------------------------------------------------
# BR02 – The email must contain the @ character
# FR02 – The system must validate whether the email is valid
# FR04 – The system must raise an exception in case of a failure
# -------------------------------------------------------------------------

def test_register_user_email_without_at_symbol_raises_exception(user_service):
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    # FR04 – The system must raise an exception in case of a failure
    
    # Arrange
    name = "Alice"
    email = "aliceexample.com" # Missing '@'
    password = "password123"
    
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name, email, password)

def test_register_user_email_with_at_symbol_is_accepted(user_service):
    # BR02 – The email must contain the @ character
    # FR02 – The system must validate whether the email is valid
    
    # Arrange
    name = "Alice"
    email = "alice@example.com"
    password = "password123"
    
    # Act
    result = user_service.register(name, email, password)
    
    # Assert
    assert result.email == "alice@example.com"

# -------------------------------------------------------------------------
# BR03 – The password must have at least 6 characters
# FR04 – The system must raise an exception in case of a failure
# -------------------------------------------------------------------------

def test_register_user_password_five_characters_raises_exception(user_service):
    # BR03 – The password must have at least 6 characters
    # FR04 – The system must raise an exception in case of a failure
    
    # Arrange
    name = "Bob"
    email = "bob@example.com"
    password = "12345" # 5 characters (Boundary - 1)
    
    # Act & Assert
    with pytest.raises(Exception):
        user_service.register(name, email, password)

def test_register_user_password_six_characters_is_accepted(user_service):
    # BR03 – The password must have at least 6 characters
    # Edge Case: Exact boundary value
    
    # Arrange
    name = "Bob"
    email = "bob@example.com"
    password = "123456" # 6 characters (Boundary)
    
    # Act
    result = user_service.register(name, email, password)
    
    # Assert
    assert result is not None

# -------------------------------------------------------------------------
# BR04 – It is not allowed to register two users with the same email
# FR03 – The system must prevent registration with a duplicate email
# FR04 – The system must raise an exception in case of a failure
# -------------------------------------------------------------------------

def test_register_duplicate_email_raises_exception(user_service):
    # BR04 – It is not allowed to register two users with the same email
    # FR03 – The system must prevent registration with a duplicate email
    # FR04 – The system must raise an exception in case of a failure
    
    # Arrange
    name_1 = "User One"
    email_shared = "duplicate@example.com"
    password_1 = "password123"
    
    name_2 = "User Two"
    # email_shared is reused
    password_2 = "differentpass"
    
    # Act - First Registration (Should Succeed)
    user_service.register(name_1, email_shared, password_1)
    
    # Act & Assert - Second Registration (Should Fail)
    with pytest.raises(Exception):
        user_service.register(name_2, email_shared, password_2)
