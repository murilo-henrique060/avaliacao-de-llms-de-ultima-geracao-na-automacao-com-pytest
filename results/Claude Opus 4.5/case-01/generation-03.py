
"""
Automated Test Cases for User Registration System
Based on formal specifications provided.
"""

import pytest


# =============================================================================
# FIXTURES
# =============================================================================

@pytest.fixture
def user_service():
    """Fixture to provide a fresh UserService instance for each test."""
    from cases.case01 import UserService
    return UserService()


@pytest.fixture
def valid_user_data():
    """Fixture providing valid user registration data."""
    return {
        "name": "John Doe",
        "email": "john.doe@example. com",
        "password": "secure123"
    }


# =============================================================================
# BR01 - All users must have a name, email, and password
# =============================================================================

# BR01 – All users must have a name, email, and password
def test_br01_register_user_with_all_required_fields_succeeds(user_service, valid_user_data):
    """Test that registration succeeds when name, email, and password are provided."""
    user = user_service.register(
        name=valid_user_data["name"],
        email=valid_user_data["email"],
        password=valid_user_data["password"]
    )
    assert user.name == valid_user_data["name"]
    assert user.email == valid_user_data["email"]


# BR01 – All users must have a name, email, and password
def test_br01_register_user_without_name_raises_exception(user_service):
    """Test that registration fails when name is not provided."""
    with pytest.raises(Exception):
        user_service. register(
            name=None,
            email="test@example.com",
            password="secure123"
        )


# BR01 – All users must have a name, email, and password
def test_br01_register_user_with_empty_name_raises_exception(user_service):
    """Test that registration fails when name is empty string."""
    with pytest.raises(Exception):
        user_service.register(
            name="",
            email="test@example.com",
            password="secure123"
        )


# BR01 – All users must have a name, email, and password
def test_br01_register_user_without_email_raises_exception(user_service):
    """Test that registration fails when email is not provided."""
    with pytest.raises(Exception):
        user_service.register(
            name="John Doe",
            email=None,
            password="secure123"
        )


# BR01 – All users must have a name, email, and password
def test_br01_register_user_with_empty_email_raises_exception(user_service):
    """Test that registration fails when email is empty string."""
    with pytest.raises(Exception):
        user_service.register(
            name="John Doe",
            email="",
            password="secure123"
        )


# BR01 – All users must have a name, email, and password
def test_br01_register_user_without_password_raises_exception(user_service):
    """Test that registration fails when password is not provided."""
    with pytest.raises(Exception):
        user_service.register(
            name="John Doe",
            email="test@example.com",
            password=None
        )


# BR01 – All users must have a name, email, and password
def test_br01_register_user_with_empty_password_raises_exception(user_service):
    """Test that registration fails when password is empty string."""
    with pytest.raises(Exception):
        user_service.register(
            name="John Doe",
            email="test@example.com",
            password=""
        )


# =============================================================================
# BR02 - The email must contain the @ character
# =============================================================================

# BR02 – Email must contain the @ character
def test_br02_register_user_with_email_containing_at_symbol_succeeds(user_service):
    """Test that registration succeeds when email contains @ character."""
    user = user_service.register(
        name="Jane Doe",
        email="jane@example.com",
        password="password123"
    )
    assert user. email == "jane@example.com"


# BR02 – Email must contain the @ character
def test_br02_register_user_with_email_missing_at_symbol_raises_exception(user_service):
    """Test that registration fails when email does not contain @ character."""
    with pytest. raises(Exception):
        user_service. register(
            name="John Doe",
            email="johnexample.com",
            password="secure123"
        )


# BR02 – Email must contain the @ character
def test_br02_register_user_with_email_containing_only_at_symbol_succeeds(user_service):
    """Test that registration succeeds when email contains only @ character (edge case for @ presence)."""
    user = user_service. register(
        name="Test User",
        email="@",
        password="secure123"
    )
    assert "@" in user.email


# =============================================================================
# BR03 - The password must have at least 6 characters
# =============================================================================

# BR03 – The password must have at least 6 characters
def test_br03_register_user_with_password_exactly_6_characters_succeeds(user_service):
    """Test that registration succeeds when password has exactly 6 characters."""
    user = user_service.register(
        name="John Doe",
        email="john@example.com",
        password="123456"
    )
    assert user is not None


# BR03 – The password must have at least 6 characters
def test_br03_register_user_with_password_more_than_6_characters_succeeds(user_service):
    """Test that registration succeeds when password has more than 6 characters."""
    user = user_service.register(
        name="John Doe",
        email="john2@example.com",
        password="1234567890"
    )
    assert user is not None


# BR03 – The password must have at least 6 characters
def test_br03_register_user_with_password_5_characters_raises_exception(user_service):
    """Test that registration fails when password has exactly 5 characters."""
    with pytest. raises(Exception):
        user_service. register(
            name="John Doe",
            email="john@example.com",
            password="12345"
        )


# BR03 – The password must have at least 6 characters
def test_br03_register_user_with_password_1_character_raises_exception(user_service):
    """Test that registration fails when password has only 1 character."""
    with pytest. raises(Exception):
        user_service. register(
            name="John Doe",
            email="john@example.com",
            password="a"
        )


# =============================================================================
# BR04 - It is not allowed to register two users with the same email
# =============================================================================

# BR04 – It is not allowed to register two users with the same email
def test_br04_register_user_with_unique_email_succeeds(user_service):
    """Test that registration succeeds when email is unique."""
    user = user_service.register(
        name="First User",
        email="unique@example.com",
        password="secure123"
    )
    assert user. email == "unique@example.com"


# BR04 – It is not allowed to register two users with the same email
def test_br04_register_second_user_with_same_email_raises_exception(user_service):
    """Test that registration fails when attempting to register with duplicate email."""
    user_service.register(
        name="First User",
        email="duplicate@example.com",
        password="secure123"
    )
    with pytest. raises(Exception):
        user_service. register(
            name="Second User",
            email="duplicate@example.com",
            password="different456"
        )


# BR04 – It is not allowed to register two users with the same email
def test_br04_register_users_with_different_emails_succeeds(user_service):
    """Test that registration succeeds for multiple users with different emails."""
    user1 = user_service. register(
        name="User One",
        email="user1@example. com",
        password="secure123"
    )
    user2 = user_service.register(
        name="User Two",
        email="user2@example. com",
        password="secure456"
    )
    assert user1.email == "user1@example.com"
    assert user2.email == "user2@example.com"


# =============================================================================
# FR01 - The system must allow registering a user
# =============================================================================

# FR01 – The system must allow registering a user
def test_fr01_register_valid_user_returns_user_object(user_service, valid_user_data):
    """Test that register method returns a User object when valid data is provided."""
    user = user_service.register(
        name=valid_user_data["name"],
        email=valid_user_data["email"],
        password=valid_user_data["password"]
    )
    assert user is not None


# FR01 – The system must allow registering a user
def test_fr01_registered_user_has_correct_name(user_service, valid_user_data):
    """Test that registered user has the correct name attribute."""
    user = user_service.register(
        name=valid_user_data["name"],
        email=valid_user_data["email"],
        password=valid_user_data["password"]
    )
    assert user. name == valid_user_data["name"]


# FR01 – The system must allow registering a user
def test_fr01_registered_user_has_correct_email(user_service, valid_user_data):
    """Test that registered user has the correct email attribute."""
    user = user_service.register(
        name=valid_user_data["name"],
        email=valid_user_data["email"],
        password=valid_user_data["password"]
    )
    assert user.email == valid_user_data["email"]


# =============================================================================
# FR02 - The system must validate whether the email is valid
# =============================================================================

# FR02 – The system must validate whether the email is valid
def test_fr02_email_validation_accepts_valid_email_with_at_symbol(user_service):
    """Test that email validation accepts an email containing @ character."""
    user = user_service.register(
        name="Valid Email User",
        email="valid@domain.com",
        password="secure123"
    )
    assert user.email == "valid@domain. com"


# FR02 – The system must validate whether the email is valid
def test_fr02_email_validation_rejects_email_without_at_symbol(user_service):
    """Test that email validation rejects an email not containing @ character."""
    with pytest.raises(Exception):
        user_service.register(
            name="Invalid Email User",
            email="invaliddomain.com",
            password="secure123"
        )


# =============================================================================
# FR03 - The system must prevent registration with a duplicate email
# =============================================================================

# FR03 – The system must prevent registration with a duplicate email
def test_fr03_duplicate_email_prevention_first_registration_succeeds(user_service):
    """Test that first registration with an email succeeds."""
    user = user_service. register(
        name="First Registration",
        email="test@duplicate.com",
        password="secure123"
    )
    assert user.email == "test@duplicate. com"


# FR03 – The system must prevent registration with a duplicate email
def test_fr03_duplicate_email_prevention_second_registration_fails(user_service):
    """Test that second registration with the same email is prevented."""
    user_service.register(
        name="First Registration",
        email="prevent@duplicate.com",
        password="secure123"
    )
    with pytest. raises(Exception):
        user_service. register(
            name="Second Registration",
            email="prevent@duplicate.com",
            password="another456"
        )


# =============================================================================
# FR04 - The system must raise an exception in case of a failure
# =============================================================================

# FR04 – The system must raise an exception in case of a failure
def test_fr04_exception_raised_when_name_is_missing(user_service):
    """Test that an exception is raised when name is missing."""
    with pytest.raises(Exception):
        user_service.register(
            name=None,
            email="test@example.com",
            password="secure123"
        )


# FR04 – The system must raise an exception in case of a failure
def test_fr04_exception_raised_when_email_is_invalid(user_service):
    """Test that an exception is raised when email is invalid (missing @)."""
    with pytest.raises(Exception):
        user_service.register(
            name="Test User",
            email="invalidemail",
            password="secure123"
        )


# FR04 – The system must raise an exception in case of a failure
def test_fr04_exception_raised_when_password_is_too_short(user_service):
    """Test that an exception is raised when password is too short."""
    with pytest.raises(Exception):
        user_service.register(
            name="Test User",
            email="test@example.com",
            password="short"
        )


# FR04 – The system must raise an exception in case of a failure
def test_fr04_exception_raised_when_email_is_duplicate(user_service):
    """Test that an exception is raised when email is duplicate."""
    user_service. register(
        name="First User",
        email="exception@test.com",
        password="secure123"
    )
    with pytest.raises(Exception):
        user_service.register(
            name="Second User",
            email="exception@test. com",
            password="secure456"
        )
