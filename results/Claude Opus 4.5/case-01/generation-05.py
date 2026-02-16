
"""
Automated Test Cases for User Registration System
Based exclusively on provided formal specifications.
"""

import pytest

# Assuming the following imports would be available from the system under test
# from user_system import User, UserService


class TestBR01AllFieldsRequired:
    """Tests for BR01: All users must have a name, email, and password."""

    # BR01 – All users must have a name, email, and password (missing name)
    def test_register_user_without_name_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service. register(name=None, email="user@example.com", password="123456")

    # BR01 – All users must have a name, email, and password (empty name)
    def test_register_user_with_empty_name_raises_exception(self, user_service):
        with pytest. raises(Exception):
            user_service. register(name="", email="user@example.com", password="123456")

    # BR01 – All users must have a name, email, and password (missing email)
    def test_register_user_without_email_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="John Doe", email=None, password="123456")

    # BR01 – All users must have a name, email, and password (empty email)
    def test_register_user_with_empty_email_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="John Doe", email="", password="123456")

    # BR01 – All users must have a name, email, and password (missing password)
    def test_register_user_without_password_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="John Doe", email="user@example.com", password=None)

    # BR01 – All users must have a name, email, and password (empty password)
    def test_register_user_with_empty_password_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="John Doe", email="user@example.com", password="")

    # BR01 – All users must have a name, email, and password (valid case)
    def test_register_user_with_all_fields_succeeds(self, user_service):
        user = user_service.register(name="John Doe", email="john@example.com", password="123456")
        assert user is not None
        assert user.name == "John Doe"
        assert user.email == "john@example.com"


class TestBR02EmailMustContainAtCharacter:
    """Tests for BR02: The email must contain the @ character."""

    # BR02 – Email must contain the @ character (missing @)
    def test_register_user_with_email_without_at_character_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="John Doe", email="userexample.com", password="123456")

    # BR02 – Email must contain the @ character (valid email with @)
    def test_register_user_with_email_containing_at_character_succeeds(self, user_service):
        user = user_service.register(name="Jane Doe", email="jane@example.com", password="123456")
        assert user is not None
        assert user.email == "jane@example. com"

    # BR02 – Email must contain the @ character (@ at the beginning)
    def test_register_user_with_email_at_character_at_beginning(self, user_service):
        user = user_service.register(name="Test User", email="@example.com", password="123456")
        assert user is not None
        assert user.email == "@example.com"

    # BR02 – Email must contain the @ character (@ at the end)
    def test_register_user_with_email_at_character_at_end(self, user_service):
        user = user_service.register(name="Test User", email="user@", password="123456")
        assert user is not None
        assert user.email == "user@"

    # BR02 – Email must contain the @ character (only @)
    def test_register_user_with_email_only_at_character(self, user_service):
        user = user_service.register(name="Test User", email="@", password="123456")
        assert user is not None
        assert user.email == "@"


class TestBR03PasswordMinimumLength: 
    """Tests for BR03: The password must have at least 6 characters."""

    # BR03 – Password must have at least 6 characters (5 characters - boundary below)
    def test_register_user_with_password_5_characters_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="John Doe", email="john@example.com", password="12345")

    # BR03 – Password must have at least 6 characters (6 characters - exact boundary)
    def test_register_user_with_password_exactly_6_characters_succeeds(self, user_service):
        user = user_service.register(name="John Doe", email="john6@example.com", password="123456")
        assert user is not None

    # BR03 – Password must have at least 6 characters (7 characters - above boundary)
    def test_register_user_with_password_7_characters_succeeds(self, user_service):
        user = user_service.register(name="John Doe", email="john7@example.com", password="1234567")
        assert user is not None

    # BR03 – Password must have at least 6 characters (1 character)
    def test_register_user_with_password_1_character_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="John Doe", email="john@example.com", password="1")

    # BR03 – Password must have at least 6 characters (0 characters handled by BR01)
    # This is covered by BR01 empty password test


class TestBR04DuplicateEmailNotAllowed:
    """Tests for BR04: It is not allowed to register two users with the same email."""

    # BR04 – Duplicate email not allowed (first registration succeeds)
    def test_register_first_user_with_unique_email_succeeds(self, user_service):
        user = user_service.register(name="First User", email="unique@example.com", password="123456")
        assert user is not None
        assert user.email == "unique@example.com"

    # BR04 – Duplicate email not allowed (second registration with same email fails)
    def test_register_second_user_with_duplicate_email_raises_exception(self, user_service):
        user_service.register(name="First User", email="duplicate@example.com", password="123456")
        with pytest. raises(Exception):
            user_service. register(name="Second User", email="duplicate@example.com", password="654321")

    # BR04 – Duplicate email not allowed (different emails succeed)
    def test_register_two_users_with_different_emails_succeeds(self, user_service):
        user1 = user_service.register(name="User One", email="user1@example.com", password="123456")
        user2 = user_service. register(name="User Two", email="user2@example.com", password="123456")
        assert user1 is not None
        assert user2 is not None
        assert user1.email != user2.email


class TestFR01SystemMustAllowRegisteringUser: 
    """Tests for FR01: The system must allow registering a user."""

    # FR01 – System must allow registering a user (successful registration)
    def test_register_user_returns_user_object(self, user_service):
        user = user_service. register(name="Valid User", email="valid@example.com", password="123456")
        assert user is not None

    # FR01 – System must allow registering a user (returned user has correct name)
    def test_register_user_returns_user_with_correct_name(self, user_service):
        user = user_service.register(name="Correct Name", email="correct@example.com", password="123456")
        assert user. name == "Correct Name"

    # FR01 – System must allow registering a user (returned user has correct email)
    def test_register_user_returns_user_with_correct_email(self, user_service):
        user = user_service.register(name="Email User", email="email@example.com", password="123456")
        assert user. email == "email@example.com"


class TestFR02SystemMustValidateEmail:
    """Tests for FR02: The system must validate whether the email is valid."""

    # FR02 – System must validate email (invalid email without @ raises exception)
    def test_system_validates_email_without_at_character_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="Invalid Email", email="invalidemail. com", password="123456")

    # FR02 – System must validate email (valid email with @ is accepted)
    def test_system_validates_email_with_at_character_succeeds(self, user_service):
        user = user_service.register(name="Valid Email", email="valid@email.com", password="123456")
        assert user is not None


class TestFR03SystemMustPreventDuplicateEmail:
    """Tests for FR03: The system must prevent registration with a duplicate email."""

    # FR03 – System must prevent duplicate email registration
    def test_system_prevents_duplicate_email_registration(self, user_service):
        user_service.register(name="Original User", email="original@example.com", password="123456")
        with pytest.raises(Exception):
            user_service.register(name="Duplicate User", email="original@example.com", password="654321")


class TestFR04SystemMustRaiseExceptionOnFailure:
    """Tests for FR04: The system must raise an exception in case of a failure."""

    # FR04 – System raises exception on missing name
    def test_system_raises_exception_when_name_is_missing(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name=None, email="test@example.com", password="123456")

    # FR04 – System raises exception on missing email
    def test_system_raises_exception_when_email_is_missing(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="Test User", email=None, password="123456")

    # FR04 – System raises exception on missing password
    def test_system_raises_exception_when_password_is_missing(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="Test User", email="test@example.com", password=None)

    # FR04 – System raises exception on invalid email
    def test_system_raises_exception_when_email_is_invalid(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="Test User", email="invalidemail", password="123456")

    # FR04 – System raises exception on short password
    def test_system_raises_exception_when_password_is_too_short(self, user_service):
        with pytest.raises(Exception):
            user_service.register(name="Test User", email="test@example.com", password="12345")

    # FR04 – System raises exception on duplicate email
    def test_system_raises_exception_when_email_is_duplicate(self, user_service):
        user_service.register(name="First", email="dup@example.com", password="123456")
        with pytest.raises(Exception):
            user_service.register(name="Second", email="dup@example.com", password="123456")


# Fixture to provide a fresh UserService instance for each test
@pytest.fixture
def user_service():
    """
    Provides a fresh UserService instance for each test. 
    This fixture assumes UserService is imported from the system under test. 
    """
    from cases.case01 import UserService
    return UserService()
