
import pytest

# -------------------------------------------------------------------------
# ASSUMPTION: The following classes are available in the system under test.
# Since implementation is forbidden, these are assumed to be imported.
# from system.models import User
# from system.services import UserService
# -------------------------------------------------------------------------

@pytest.fixture
def user_service():
    """
    Provides a fresh instance of UserService for each test to ensure isolation.
    """
    # Ideally returns: UserService()
    # For the purpose of this test generation, we assume the class exists.
    from cases.case01 import UserService  # type: ignore
    return UserService()

class TestUserRegistration:

    def test_fr01_br01_br02_br03_register_valid_user_success(self, user_service):
        # FR01 - The system must allow registering a user
        # BR01 - All users must have a name, email, and password
        # BR02 - The email must contain the @ character
        # BR03 - The password must have at least 6 characters
        name = "John Doe"
        email = "john.doe@example.com"
        password = "securePassword123"

        user = user_service.register(name, email, password)

        assert user is not None
        assert user.name == name
        assert user.email == email
        # Password is private in UML (-password), checking public attributes only if exposed,
        # or assuming the object creation was successful.

    def test_br01_fr04_register_missing_name_raises_exception(self, user_service):
        # BR01 - All users must have a name
        # FR04 - The system must raise an exception in case of a failure
        name = None
        email = "john.doe@example.com"
        password = "securePassword123"

        with pytest.raises(Exception):
            user_service.register(name, email, password)

    def test_br01_fr04_register_missing_email_raises_exception(self, user_service):
        # BR01 - All users must have an email
        # FR04 - The system must raise an exception in case of a failure
        name = "John Doe"
        email = None
        password = "securePassword123"

        with pytest.raises(Exception):
            user_service.register(name, email, password)

    def test_br01_fr04_register_missing_password_raises_exception(self, user_service):
        # BR01 - All users must have a password
        # FR04 - The system must raise an exception in case of a failure
        name = "John Doe"
        email = "john.doe@example.com"
        password = None

        with pytest.raises(Exception):
            user_service.register(name, email, password)

    def test_br02_fr02_fr04_register_email_without_at_character_raises_exception(self, user_service):
        # BR02 - The email must contain the @ character
        # FR02 - The system must validate whether the email is valid
        # FR04 - The system must raise an exception in case of a failure
        name = "John Doe"
        email = "johndoeexample.com"  # Missing @
        password = "securePassword123"

        with pytest.raises(Exception):
            user_service.register(name, email, password)

    def test_br03_fr04_register_password_less_than_six_chars_raises_exception(self, user_service):
        # BR03 - The password must have at least 6 characters
        # FR04 - The system must raise an exception in case of a failure
        name = "John Doe"
        email = "john.doe@example.com"
        password = "12345"  # 5 characters

        with pytest.raises(Exception):
            user_service.register(name, email, password)

    def test_br03_register_password_exactly_six_chars_success(self, user_service):
        # BR03 - The password must have at least 6 characters (Edge Case: Exactly 6)
        # FR01 - The system must allow registering a user
        name = "John Doe"
        email = "john.doe@example.com"
        password = "123456"  # Exactly 6 characters

        user = user_service.register(name, email, password)

        assert user is not None
        assert user.email == email

    def test_br04_fr03_fr04_register_duplicate_email_raises_exception(self, user_service):
        # BR04 - It is not allowed to register two users with the same email
        # FR03 - The system must prevent registration with a duplicate email
        # FR04 - The system must raise an exception in case of a failure
        name1 = "User One"
        email = "common@example.com"
        password = "password123"
        
        # First registration (Success)
        user_service.register(name1, email, password)

        # Second registration with same email (Failure)
        name2 = "User Two"
        
        with pytest.raises(Exception):
            user_service.register(name2, email, password)
