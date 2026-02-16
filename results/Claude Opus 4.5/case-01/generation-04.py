
"""
Automated tests for User Registration System
Based on Business Rules (BR01-BR04) and Functional Requirements (FR01-FR04)
"""

import pytest


# =============================================================================
# BUSINESS RULE 01 (BR01) - All users must have a name, email, and password
# =============================================================================

# BR01 – All users must have a name, email, and password (positive case)
def test_br01_register_user_with_all_required_fields_succeeds():
    from cases.case01 import UserService

    service = UserService()
    user = service.register(name="John Doe", email="john@example.com", password="secret123")
    
    assert user.name == "John Doe"
    assert user.email == "john@example.com"


# BR01 – All users must have a name, email, and password (missing name)
def test_br01_register_user_without_name_raises_exception():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="", email="john@example.com", password="secret123")


# BR01 – All users must have a name, email, and password (name is None)
def test_br01_register_user_with_none_name_raises_exception():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name=None, email="john@example.com", password="secret123")


# BR01 – All users must have a name, email, and password (missing email)
def test_br01_register_user_without_email_raises_exception():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="John Doe", email="", password="secret123")


# BR01 – All users must have a name, email, and password (email is None)
def test_br01_register_user_with_none_email_raises_exception():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="John Doe", email=None, password="secret123")


# BR01 – All users must have a name, email, and password (missing password)
def test_br01_register_user_without_password_raises_exception():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="John Doe", email="john@example.com", password="")


# BR01 – All users must have a name, email, and password (password is None)
def test_br01_register_user_with_none_password_raises_exception():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="John Doe", email="john@example.com", password=None)


# =============================================================================
# BUSINESS RULE 02 (BR02) - The email must contain the @ character
# =============================================================================

# BR02 – Email must contain the @ character (positive case)
def test_br02_register_user_with_email_containing_at_symbol_succeeds():
    from user_service import UserService
    
    service = UserService()
    user = service.register(name="Jane Doe", email="jane@domain.com", password="password123")
    
    assert "@" in user.email


# BR02 – Email must contain the @ character (missing @ symbol)
def test_br02_register_user_with_email_missing_at_symbol_raises_exception():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="Jane Doe", email="janedomain.com", password="password123")


# BR02 – Email must contain the @ character (email with only @ symbol)
def test_br02_register_user_with_email_containing_only_at_symbol_succeeds():
    from user_service import UserService
    
    service = UserService()
    user = service.register(name="Test User", email="@", password="password123")
    
    assert user.email == "@"


# =============================================================================
# BUSINESS RULE 03 (BR03) - The password must have at least 6 characters
# =============================================================================

# BR03 – The password must have at least 6 characters (exactly 6 characters)
def test_br03_register_user_with_password_exactly_6_characters_succeeds():
    from user_service import UserService
    
    service = UserService()
    user = service.register(name="Alice", email="alice@test.com", password="123456")
    
    assert user is not None


# BR03 – The password must have at least 6 characters (more than 6 characters)
def test_br03_register_user_with_password_more_than_6_characters_succeeds():
    from user_service import UserService
    
    service = UserService()
    user = service.register(name="Bob", email="bob@test.com", password="1234567890")
    
    assert user is not None


# BR03 – The password must have at least 6 characters (5 characters - boundary)
def test_br03_register_user_with_password_5_characters_raises_exception():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="Charlie", email="charlie@test.com", password="12345")


# BR03 – The password must have at least 6 characters (1 character)
def test_br03_register_user_with_password_1_character_raises_exception():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="David", email="david@test.com", password="a")


# =============================================================================
# BUSINESS RULE 04 (BR04) - It is not allowed to register two users with the same email
# =============================================================================

# BR04 – It is not allowed to register two users with the same email (positive case - unique emails)
def test_br04_register_two_users_with_different_emails_succeeds():
    from user_service import UserService
    
    service = UserService()
    user1 = service.register(name="User One", email="user1@test.com", password="password1")
    user2 = service.register(name="User Two", email="user2@test.com", password="password2")
    
    assert user1.email != user2.email


# BR04 – It is not allowed to register two users with the same email (duplicate email)
def test_br04_register_user_with_duplicate_email_raises_exception():
    from user_service import UserService
    
    service = UserService()
    service.register(name="First User", email="duplicate@test.com", password="password1")
    
    with pytest.raises(Exception):
        service.register(name="Second User", email="duplicate@test.com", password="password2")


# =============================================================================
# FUNCTIONAL REQUIREMENT 01 (FR01) - The system must allow registering a user
# =============================================================================

# FR01 – The system must allow registering a user
def test_fr01_system_allows_registering_valid_user():
    from user_service import UserService
    from user import User
    
    service = UserService()
    user = service.register(name="Valid User", email="valid@email.com", password="validpassword")
    
    assert isinstance(user, User)


# FR01 – The system must allow registering a user (verify returned user has correct name)
def test_fr01_registered_user_has_correct_name():
    from user_service import UserService
    
    service = UserService()
    user = service.register(name="Expected Name", email="name@test.com", password="password123")
    
    assert user.name == "Expected Name"


# FR01 – The system must allow registering a user (verify returned user has correct email)
def test_fr01_registered_user_has_correct_email():
    from user_service import UserService
    
    service = UserService()
    user = service.register(name="Email User", email="expected@email.com", password="password123")
    
    assert user. email == "expected@email.com"


# =============================================================================
# FUNCTIONAL REQUIREMENT 02 (FR02) - The system must validate whether the email is valid
# =============================================================================

# FR02 – The system must validate whether the email is valid (valid email with @)
def test_fr02_system_validates_email_with_at_symbol_as_valid():
    from user_service import UserService
    
    service = UserService()
    user = service. register(name="Validated User", email="validated@domain.com", password="securepass")
    
    assert user is not None
    assert "@" in user.email


# FR02 – The system must validate whether the email is valid (invalid email without @)
def test_fr02_system_rejects_email_without_at_symbol():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="Invalid Email User", email="invalidemail. com", password="securepass")


# =============================================================================
# FUNCTIONAL REQUIREMENT 03 (FR03) - The system must prevent registration with a duplicate email
# =============================================================================

# FR03 – The system must prevent registration with a duplicate email
def test_fr03_system_prevents_duplicate_email_registration():
    from user_service import UserService
    
    service = UserService()
    service.register(name="Original User", email="unique@email.com", password="password123")
    
    with pytest. raises(Exception):
        service.register(name="Duplicate User", email="unique@email.com", password="different123")


# FR03 – The system must prevent registration with a duplicate email (first registration succeeds)
def test_fr03_first_registration_with_email_succeeds():
    from user_service import UserService
    
    service = UserService()
    user = service.register(name="First Registration", email="first@email.com", password="password123")
    
    assert user. email == "first@email.com"


# =============================================================================
# FUNCTIONAL REQUIREMENT 04 (FR04) - The system must raise an exception in case of a failure
# =============================================================================

# FR04 – The system must raise an exception in case of a failure (invalid email)
def test_fr04_system_raises_exception_for_invalid_email():
    from user_service import UserService
    
    service = UserService()
    
    with pytest. raises(Exception):
        service.register(name="Test User", email="noemail", password="password123")


# FR04 – The system must raise an exception in case of a failure (short password)
def test_fr04_system_raises_exception_for_short_password():
    from user_service import UserService
    
    service = UserService()
    
    with pytest.raises(Exception):
        service.register(name="Test User", email="test@email.com", password="short")


# FR04 – The system must raise an exception in case of a failure (missing name)
def test_fr04_system_raises_exception_for_missing_name():
    from user_service import UserService
    
    service = UserService()
    
    with pytest. raises(Exception):
        service.register(name="", email="test@email.com", password="password123")


# FR04 – The system must raise an exception in case of a failure (duplicate email)
def test_fr04_system_raises_exception_for_duplicate_email():
    from user_service import UserService
    
    service = UserService()
    service.register(name="Existing User", email="exists@email.com", password="password123")
    
    with pytest.raises(Exception):
        service.register(name="New User", email="exists@email.com", password="newpassword")
