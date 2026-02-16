import pytest

from cases.case01 import UserService, User

# BR01 – All users must have a name, email, and password
def test_br01_all_fields_present_registers_successfully():
    service = UserService()
    # Validate behavior: registration succeeds when name, email, and password are provided
    user = service.register(name="Alice", email="alice@example.com", password="strongpwd")
    assert isinstance(user, User)

# BR01 – All users must have a name, email, and password
def test_br01_missing_name_raises_exception():
    service = UserService()
    # Validate behavior: registration fails when name is missing
    with pytest.raises(Exception):
        service.register(name="", email="bob@example.com", password="strongpwd")

# BR01 – All users must have a name, email, and password
def test_br01_missing_email_raises_exception():
    service = UserService()
    # Validate behavior: registration fails when email is missing
    with pytest.raises(Exception):
        service.register(name="Bob", email="", password="strongpwd")

# BR01 – All users must have a name, email, and password
def test_br01_missing_password_raises_exception():
    service = UserService()
    # Validate behavior: registration fails when password is missing
    with pytest.raises(Exception):
        service.register(name="Carol", email="carol@example.com", password="")

# BR02 – Email must contain the @ character
def test_br02_email_without_at_symbol_raises_exception():
    service = UserService()
    # Validate behavior: registration fails when email does not contain '@'
    with pytest.raises(Exception):
        service.register(name="Dave", email="dave.example.com", password="strongpwd")

# BR02 – Email must contain the @ character
def test_br02_email_with_at_registers_successfully():
    service = UserService()
    # Validate behavior: registration succeeds when email contains '@'
    user = service.register(name="Eve", email="eve@domain.com", password="strongpwd")
    assert isinstance(user, User)

# BR03 – The password must have at least 6 characters
def test_br03_password_too_short_raises_exception():
    service = UserService()
    # Validate behavior: registration fails when password has fewer than 6 characters (5 provided)
    with pytest.raises(Exception):
        service.register(name="Frank", email="frank@example.com", password="abcde")

# BR03 – The password must have at least 6 characters
def test_br03_password_exactly_six_registers_successfully():
    service = UserService()
    # Validate behavior (edge case): registration succeeds when password has exactly 6 characters
    user = service.register(name="Grace", email="grace@example.com", password="abcdef")
    assert isinstance(user, User)

# BR04 – It is not allowed to register two users with the same email
def test_br04_duplicate_email_registration_raises_exception():
    service = UserService()
    # Validate behavior: second registration with the same email must fail
    service.register(name="Heidi", email="heidi@example.com", password="strongpwd")
    with pytest.raises(Exception):
        service.register(name="HeidiClone", email="heidi@example.com", password="anotherpwd")

# FR01 – The system must allow registering a user
def test_fr01_register_returns_user_instance_for_valid_input():
    service = UserService()
    # Validate behavior: register returns a User instance for valid input
    user = service.register(name="Ivy", email="ivy@example.com", password="strongpwd")
    assert isinstance(user, User)

# FR02 – The system must validate whether the email is valid
def test_fr02_invalid_email_validation_raises_exception():
    service = UserService()
    # Validate behavior: system rejects invalid email formats (no '@') by raising an exception
    with pytest.raises(Exception):
        service.register(name="Jack", email="jack.example.com", password="strongpwd")

# FR03 – The system must prevent registration with a duplicate email
def test_fr03_prevents_duplicate_email_registration():
    service = UserService()
    # Validate behavior: system prevents registering two users with identical emails by raising an exception
    service.register(name="Kate", email="kate@example.com", password="strongpwd")
    with pytest.raises(Exception):
        service.register(name="Kate2", email="kate@example.com", password="strongpwd2")

# FR04 – The system must raise an exception in case of a failure
def test_fr04_failure_raises_exception_on_password_too_short():
    service = UserService()
    # Validate behavior: system raises an exception when registration fails (password too short used as failure)
    with pytest.raises(Exception):
        service.register(name="Leo", email="leo@example.com", password="12345")