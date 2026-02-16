"""
Automated tests for User Registration System
Based on provided Business Rules (BR) and Functional Requirements (FR)
"""

import pytest

# Assuming the following imports from the system under test
# from user_system import User, UserService


class TestBR01AllFieldsRequired:
    """Tests for BR01: All users must have a name, email, and password"""

    # BR01 – All users must have a name, email, and password (valid case)
    def test_register_user_with_all_required_fields_succeeds(self, user_service):
        user = user_service. register(
            name="John Doe",
            email="john@example.com",
            password="secure123"
        )
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    # BR01 – All users must have a name (missing name)
    def test_register_user_without_name_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name=None,
                email="john@example.com",
                password="secure123"
            )

    # BR01 – All users must have a name (empty name)
    def test_register_user_with_empty_name_raises_exception(self, user_service):
        with pytest. raises(Exception):
            user_service. register(
                name="",
                email="john@example. com",
                password="secure123"
            )

    # BR01 – All users must have an email (missing email)
    def test_register_user_without_email_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="John Doe",
                email=None,
                password="secure123"
            )

    # BR01 – All users must have an email (empty email)
    def test_register_user_with_empty_email_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="John Doe",
                email="",
                password="secure123"
            )

    # BR01 – All users must have a password (missing password)
    def test_register_user_without_password_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="John Doe",
                email="john@example.com",
                password=None
            )

    # BR01 – All users must have a password (empty password)
    def test_register_user_with_empty_password_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="John Doe",
                email="john@example.com",
                password=""
            )


class TestBR02EmailMustContainAtCharacter:
    """Tests for BR02: The email must contain the @ character"""

    # BR02 – Email must contain the @ character (valid case)
    def test_register_user_with_email_containing_at_character_succeeds(self, user_service):
        user = user_service.register(
            name="Jane Doe",
            email="jane@domain.com",
            password="password123"
        )
        assert user. email == "jane@domain.com"

    # BR02 – Email must contain the @ character (missing @ character)
    def test_register_user_with_email_without_at_character_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Jane Doe",
                email="janedomain.com",
                password="password123"
            )

    # BR02 – Email must contain the @ character (email is just text without @)
    def test_register_user_with_plain_text_email_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Jane Doe",
                email="notanemail",
                password="password123"
            )


class TestBR03PasswordMinimumLength: 
    """Tests for BR03: The password must have at least 6 characters"""

    # BR03 – Password must have at least 6 characters (exactly 6 characters - boundary)
    def test_register_user_with_password_of_exactly_6_characters_succeeds(self, user_service):
        user = user_service.register(
            name="Bob Smith",
            email="bob@example.com",
            password="123456"
        )
        assert user. name == "Bob Smith"

    # BR03 – Password must have at least 6 characters (more than 6 characters)
    def test_register_user_with_password_of_more_than_6_characters_succeeds(self, user_service):
        user = user_service.register(
            name="Bob Smith",
            email="bob2@example.com",
            password="1234567890"
        )
        assert user.name == "Bob Smith"

    # BR03 – Password must have at least 6 characters (5 characters - boundary violation)
    def test_register_user_with_password_of_5_characters_raises_exception(self, user_service):
        with pytest. raises(Exception):
            user_service. register(
                name="Bob Smith",
                email="bob@example.com",
                password="12345"
            )

    # BR03 – Password must have at least 6 characters (1 character)
    def test_register_user_with_password_of_1_character_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Bob Smith",
                email="bob@example.com",
                password="a"
            )


class TestBR04NoDuplicateEmails:
    """Tests for BR04: It is not allowed to register two users with the same email"""

    # BR04 – No duplicate emails allowed (first registration succeeds)
    def test_register_first_user_with_unique_email_succeeds(self, user_service):
        user = user_service.register(
            name="Alice Johnson",
            email="alice@unique.com",
            password="password123"
        )
        assert user.email == "alice@unique. com"

    # BR04 – No duplicate emails allowed (second registration with same email fails)
    def test_register_second_user_with_same_email_raises_exception(self, user_service):
        user_service.register(
            name="First User",
            email="duplicate@example.com",
            password="password123"
        )
        with pytest. raises(Exception):
            user_service. register(
                name="Second User",
                email="duplicate@example.com",
                password="different456"
            )

    # BR04 – No duplicate emails allowed (different emails are allowed)
    def test_register_two_users_with_different_emails_succeeds(self, user_service):
        user1 = user_service.register(
            name="User One",
            email="user1@example.com",
            password="password123"
        )
        user2 = user_service.register(
            name="User Two",
            email="user2@example.com",
            password="password456"
        )
        assert user1.email == "user1@example.com"
        assert user2.email == "user2@example.com"


class TestFR01SystemAllowsUserRegistration:
    """Tests for FR01: The system must allow registering a user"""

    # FR01 – System must allow registering a user
    def test_system_allows_registering_valid_user(self, user_service):
        user = user_service.register(
            name="Charlie Brown",
            email="charlie@example.com",
            password="secure123"
        )
        assert user is not None

    # FR01 – System must allow registering a user and return User object
    def test_register_returns_user_object_with_correct_name(self, user_service):
        user = user_service. register(
            name="Diana Prince",
            email="diana@example.com",
            password="wonder123"
        )
        assert user. name == "Diana Prince"

    # FR01 – System must allow registering a user and return User object with correct email
    def test_register_returns_user_object_with_correct_email(self, user_service):
        user = user_service.register(
            name="Edward Norton",
            email="edward@example.com",
            password="edward123"
        )
        assert user. email == "edward@example.com"


class TestFR02SystemValidatesEmail:
    """Tests for FR02: The system must validate whether the email is valid"""

    # FR02 – System must validate whether the email is valid (valid email with @)
    def test_system_accepts_valid_email_with_at_character(self, user_service):
        user = user_service. register(
            name="Frank Miller",
            email="frank@valid.com",
            password="frank123"
        )
        assert user. email == "frank@valid.com"

    # FR02 – System must validate whether the email is valid (invalid email without @)
    def test_system_rejects_invalid_email_without_at_character(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Frank Miller",
                email="frankinvalid.com",
                password="frank123"
            )


class TestFR03SystemPreventsDuplicateEmail:
    """Tests for FR03: The system must prevent registration with a duplicate email"""

    # FR03 – System must prevent registration with a duplicate email
    def test_system_prevents_duplicate_email_registration(self, user_service):
        user_service.register(
            name="Grace Hopper",
            email="grace@navy.mil",
            password="admiral123"
        )
        with pytest. raises(Exception):
            user_service. register(
                name="Grace Hopper Clone",
                email="grace@navy.mil",
                password="clone123"
            )


class TestFR04SystemRaisesExceptionOnFailure:
    """Tests for FR04: The system must raise an exception in case of a failure"""

    # FR04 – System must raise an exception in case of a failure (missing name)
    def test_system_raises_exception_when_name_is_missing(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name=None,
                email="test@example.com",
                password="test123"
            )

    # FR04 – System must raise an exception in case of a failure (missing email)
    def test_system_raises_exception_when_email_is_missing(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Test User",
                email=None,
                password="test123"
            )

    # FR04 – System must raise an exception in case of a failure (missing password)
    def test_system_raises_exception_when_password_is_missing(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Test User",
                email="test@example.com",
                password=None
            )

    # FR04 – System must raise an exception in case of a failure (invalid email)
    def test_system_raises_exception_when_email_is_invalid(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Test User",
                email="invalidemail",
                password="test123"
            )

    # FR04 – System must raise an exception in case of a failure (short password)
    def test_system_raises_exception_when_password_is_too_short(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Test User",
                email="test@example.com",
                password="short"
            )

    # FR04 – System must raise an exception in case of a failure (duplicate email)
    def test_system_raises_exception_when_email_is_duplicate(self, user_service):
        user_service.register(
            name="Original User",
            email="original@example. com",
            password="original123"
        )
        with pytest.raises(Exception):
            user_service.register(
                name="Duplicate User",
                email="original@example.com",
                password="duplicate123"
            )


# Pytest fixture for UserService
# Note: This fixture assumes the existence of UserService class from the system under test
@pytest.fixture
def user_service():
    """
    Fixture that provides a fresh UserService instance for each test.
    Each test receives an isolated instance to ensure test independence.
    """
    # Import would be:  from user_system import UserService
    # return UserService()
    
    # Placeholder:  actual implementation depends on the system under test
    from cases.case01 import UserService
    return UserService()
