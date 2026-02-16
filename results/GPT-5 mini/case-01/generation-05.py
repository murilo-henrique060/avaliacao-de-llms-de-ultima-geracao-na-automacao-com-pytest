import pytest
from cases.case01 import UserService, User

# BR01 – All users must have a name, email, and password
def test_br01_register_with_all_fields_present_succeeds():
    svc = UserService()
    user = svc.register("Alice", "alice@example.com", "password1")
    assert isinstance(user, User)

# BR01 – All users must have a name, email, and password
def test_br01_missing_name_raises_exception():
    svc = UserService()
    with pytest.raises(Exception):
        svc.register("", "bob@example.com", "password1")

# BR01 – All users must have a name, email, and password
def test_br01_missing_email_raises_exception():
    svc = UserService()
    with pytest.raises(Exception):
        svc.register("Bob", "", "password1")

# BR01 – All users must have a name, email, and password
def test_br01_missing_password_raises_exception():
    svc = UserService()
    with pytest.raises(Exception):
        svc.register("Carol", "carol@example.com", "")

# BR02 – Email must contain the @ character
def test_br02_valid_email_with_at_allows_registration():
    svc = UserService()
    user = svc.register("Dave", "dave@domain.com", "secure6")
    assert user.email == "dave@domain.com"

# BR02 – Email must contain the @ character
def test_br02_email_without_at_raises_exception():
    svc = UserService()
    with pytest.raises(Exception):
        svc.register("Eve", "eve.domain.com", "secure6")

# BR03 – The password must have at least 6 characters
def test_br03_password_with_exactly_six_characters_allows_registration():
    svc = UserService()
    user = svc.register("Frank", "frank@example.com", "123456")
    assert isinstance(user, User)

# BR03 – The password must have at least 6 characters
def test_br03_password_with_five_characters_raises_exception():
    svc = UserService()
    with pytest.raises(Exception):
        svc.register("Grace", "grace@example.com", "12345")

# BR04 – It is not allowed to register two users with the same email
def test_br04_prevent_duplicate_email_registration_raises_exception():
    svc = UserService()
    svc.register("Heidi", "heidi@example.com", "password1")
    with pytest.raises(Exception):
        svc.register("Heidi2", "heidi@example.com", "password2")

# BR04 – It is not allowed to register two users with the same email
def test_br04_allow_different_emails_for_multiple_registrations():
    svc = UserService()
    svc.register("Ivan", "ivan@example.com", "password1")
    user2 = svc.register("Judy", "judy@example.com", "password2")
    assert user2.email == "judy@example.com"

# FR01 – The system must allow registering a user
def test_fr01_register_returns_user_instance_on_success():
    svc = UserService()
    user = svc.register("Karl", "karl@example.com", "pwd1234")
    assert isinstance(user, User)

# FR02 – The system must validate whether the email is valid
def test_fr02_invalid_email_without_at_raises_exception():
    svc = UserService()
    with pytest.raises(Exception):
        svc.register("Liam", "liamexample.com", "validpw")

# FR03 – The system must prevent registration with a duplicate email
def test_fr03_registering_same_email_twice_results_in_exception():
    svc = UserService()
    svc.register("Mia", "mia@example.com", "securepw")
    with pytest.raises(Exception):
        svc.register("MiaClone", "mia@example.com", "otherpw")

# FR04 – The system must raise an exception in case of a failure
def test_fr04_system_raises_exception_on_registration_failure():
    svc = UserService()
    # Use an email string that lacks '@' to provoke a validation failure
    with pytest.raises(Exception):
        svc.register("Noah", "noathere", "password1")