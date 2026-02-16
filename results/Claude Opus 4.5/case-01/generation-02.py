
"""
Automated Test Cases for User Registration System
Based on formal specifications provided. 
"""

import pytest

# Assuming the following imports would be available from the system under test
# from user_system import User, UserService


class TestBR01AllUsersMustHaveNameEmailAndPassword: 
    """Tests for BR01: All users must have a name, email, and password."""

    # BR01 – All users must have a name, email, and password (positive case)
    def test_register_user_with_name_email_and_password_succeeds(self, user_service):
        user = user_service. register(
            name="John Doe",
            email="john@example.com",
            password="123456"
        )
        assert user.name == "John Doe"
        assert user.email == "john@example.com"

    # BR01 – All users must have a name (negative case:  missing name)
    def test_register_user_without_name_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service. register(
                name="",
                email="john@example.com",
                password="123456"
            )

    # BR01 – All users must have an email (negative case: missing email)
    def test_register_user_without_email_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="John Doe",
                email="",
                password="123456"
            )

    # BR01 – All users must have a password (negative case:  missing password)
    def test_register_user_without_password_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="John Doe",
                email="john@example.com",
                password=""
            )


class TestBR02EmailMustContainAtCharacter:
    """Tests for BR02: The email must contain the @ character."""

    # BR02 – Email must contain the @ character (positive case)
    def test_register_user_with_email_containing_at_character_succeeds(self, user_service):
        user = user_service.register(
            name="Jane Doe",
            email="jane@domain.com",
            password="654321"
        )
        assert user. email == "jane@domain.com"

    # BR02 – Email must contain the @ character (negative case: missing @)
    def test_register_user_with_email_missing_at_character_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Jane Doe",
                email="janedomain.com",
                password="654321"
            )


class TestBR03PasswordMustHaveAtLeastSixCharacters: 
    """Tests for BR03: The password must have at least 6 characters."""

    # BR03 – Password must have at least 6 characters (positive case:  exactly 6 characters)
    def test_register_user_with_password_of_exactly_six_characters_succeeds(self, user_service):
        user = user_service.register(
            name="Alice Smith",
            email="alice@example.com",
            password="abcdef"
        )
        assert user.name == "Alice Smith"

    # BR03 – Password must have at least 6 characters (positive case: more than 6 characters)
    def test_register_user_with_password_of_more_than_six_characters_succeeds(self, user_service):
        user = user_service.register(
            name="Bob Brown",
            email="bob@example.com",
            password="abcdefgh"
        )
        assert user.name == "Bob Brown"

    # BR03 – Password must have at least 6 characters (negative case: exactly 5 characters)
    def test_register_user_with_password_of_five_characters_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Charlie Green",
                email="charlie@example.com",
                password="abcde"
            )

    # BR03 – Password must have at least 6 characters (negative case: 1 character)
    def test_register_user_with_password_of_one_character_raises_exception(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="David White",
                email="david@example.com",
                password="a"
            )


class TestBR04NoDuplicateEmails:
    """Tests for BR04: It is not allowed to register two users with the same email."""

    # BR04 – It is not allowed to register two users with the same email (negative case)
    def test_register_user_with_duplicate_email_raises_exception(self, user_service):
        user_service.register(
            name="First User",
            email="duplicate@example.com",
            password="password1"
        )
        with pytest.raises(Exception):
            user_service.register(
                name="Second User",
                email="duplicate@example.com",
                password="password2"
            )

    # BR04 – Different emails should allow registration (positive case)
    def test_register_users_with_different_emails_succeeds(self, user_service):
        user1 = user_service.register(
            name="User One",
            email="user1@example.com",
            password="pass123"
        )
        user2 = user_service.register(
            name="User Two",
            email="user2@example.com",
            password="pass456"
        )
        assert user1.email == "user1@example. com"
        assert user2.email == "user2@example.com"


class TestFR01SystemMustAllowRegisteringUser:
    """Tests for FR01: The system must allow registering a user."""

    # FR01 – The system must allow registering a user (positive case)
    def test_system_allows_registering_valid_user(self, user_service):
        user = user_service.register(
            name="Valid User",
            email="valid@example. com",
            password="validpass"
        )
        assert user is not None
        assert user.name == "Valid User"
        assert user.email == "valid@example. com"


class TestFR02SystemMustValidateEmail:
    """Tests for FR02: The system must validate whether the email is valid."""

    # FR02 – The system must validate whether the email is valid (positive case)
    def test_system_accepts_valid_email_with_at_character(self, user_service):
        user = user_service.register(
            name="Email Test User",
            email="test@valid.com",
            password="testpass"
        )
        assert user. email == "test@valid.com"

    # FR02 – The system must validate whether the email is valid (negative case)
    def test_system_rejects_invalid_email_without_at_character(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Invalid Email User",
                email="invalidemail. com",
                password="testpass"
            )


class TestFR03SystemMustPreventDuplicateEmail:
    """Tests for FR03: The system must prevent registration with a duplicate email."""

    # FR03 – The system must prevent registration with a duplicate email
    def test_system_prevents_registration_with_duplicate_email(self, user_service):
        user_service.register(
            name="Original User",
            email="original@example. com",
            password="origpass"
        )
        with pytest.raises(Exception):
            user_service.register(
                name="Duplicate User",
                email="original@example.com",
                password="dupepass"
            )


class TestFR04SystemMustRaiseExceptionOnFailure: 
    """Tests for FR04: The system must raise an exception in case of a failure."""

    # FR04 – The system must raise an exception in case of failure (missing name)
    def test_system_raises_exception_when_name_is_missing(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="",
                email="exception@example.com",
                password="excpass"
            )

    # FR04 – The system must raise an exception in case of failure (missing email)
    def test_system_raises_exception_when_email_is_missing(self, user_service):
        with pytest. raises(Exception):
            user_service. register(
                name="Exception User",
                email="",
                password="excpass"
            )

    # FR04 – The system must raise an exception in case of failure (missing password)
    def test_system_raises_exception_when_password_is_missing(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Exception User",
                email="exception@example.com",
                password=""
            )

    # FR04 – The system must raise an exception in case of failure (invalid email)
    def test_system_raises_exception_when_email_is_invalid(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Exception User",
                email="invalidemailnoat",
                password="excpass"
            )

    # FR04 – The system must raise an exception in case of failure (short password)
    def test_system_raises_exception_when_password_is_too_short(self, user_service):
        with pytest.raises(Exception):
            user_service.register(
                name="Exception User",
                email="exception@example.com",
                password="short"
            )

    # FR04 – The system must raise an exception in case of failure (duplicate email)
    def test_system_raises_exception_when_email_is_duplicate(self, user_service):
        user_service.register(
            name="First Exception User",
            email="dup_exception@example.com",
            password="firstpass"
        )
        with pytest. raises(Exception):
            user_service. register(
                name="Second Exception User",
                email="dup_exception@example.com",
                password="secondpass"
            )


class TestUserClassAttributes:
    """Tests for User class attributes as defined in the class diagram."""

    # User class – name attribute is accessible (public)
    def test_user_name_attribute_is_accessible(self, user_service):
        user = user_service.register(
            name="Attribute Test",
            email="attr@example.com",
            password="attrpass"
        )
        assert hasattr(user, "name")
        assert user.name == "Attribute Test"

    # User class – email attribute is accessible (public)
    def test_user_email_attribute_is_accessible(self, user_service):
        user = user_service.register(
            name="Email Attr Test",
            email="emailattr@example.com",
            password="attrpass"
        )
        assert hasattr(user, "email")
        assert user.email == "emailattr@example. com"


# Fixture for UserService
@pytest. fixture
def user_service():
    """
    Fixture that provides a fresh UserService instance for each test.
    This ensures test isolation for BR04 (duplicate email checks).
    """
    # This would be imported from the actual system
    # from user_system import UserService
    # return UserService()
    
    # Placeholder:  the actual implementation would be provided by the system under test
    from cases.case01 import UserService
    return UserService()
