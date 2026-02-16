
import pytest
from decimal import Decimal

# Assuming the existence of the classes based on the provided Class Diagram.
# These mocks are provided to ensure the tests are semantically valid Python 
# but rely on the interface defined in the prompt.
from cases.case03 import Subscription, Payment  # type: ignore

# ----------------------------------------------------------------------------------
# FIXTURES
# ----------------------------------------------------------------------------------

@pytest.fixture
def subscription():
    """Returns a new Subscription in the default ACTIVE state."""
    sub = Subscription()
    sub.status = "ACTIVE"
    sub.payment_failures = 0
    return sub

@pytest.fixture
def success_payment():
    """Returns a Payment object representing success."""
    pay = Payment()
    pay.success = True
    return pay

@pytest.fixture
def failed_payment():
    """Returns a Payment object representing failure."""
    pay = Payment()
    pay.success = False
    return pay

# ----------------------------------------------------------------------------------
# TEST CASES
# ----------------------------------------------------------------------------------

def test_fr01_fr02_record_payment_update_status_success(subscription, success_payment):
    # FR01 - The system must record payments
    # FR02 - The system must update the subscription status based on payment success
    
    # Act
    subscription.record_payment(success_payment)

    # Assert
    assert subscription.status == "ACTIVE"
    assert subscription.payment_failures == 0

def test_fr03_increment_failure_counter(subscription, failed_payment):
    # FR03 - The system must control the number of consecutive payment failures
    # BR03 - The subscription must be automatically suspended after exactly 3 consecutive payment failures
    
    # Act
    subscription.record_payment(failed_payment)

    # Assert
    # 1 failure is not enough to suspend (Boundary Value Analysis)
    assert subscription.payment_failures == 1
    assert subscription.status == "ACTIVE"

def test_fr03_consecutive_failures_count_accumulation(subscription, failed_payment):
    # FR03 - The system must control the number of consecutive payment failures
    
    # Arrange
    subscription.record_payment(failed_payment) # 1st failure

    # Act
    subscription.record_payment(failed_payment) # 2nd failure

    # Assert
    # 2 failures are not enough to suspend (Boundary Value Analysis)
    assert subscription.payment_failures == 2
    assert subscription.status == "ACTIVE"

def test_br03_suspend_exactly_after_three_consecutive_failures(subscription, failed_payment):
    # BR01 - A subscription may be in ... SUSPENDED
    # BR03 - The subscription must be automatically suspended after exactly 3 consecutive payment failures
    # FR02 - Update subscription status based on payment success or failure
    
    # Arrange
    subscription.record_payment(failed_payment) # 1st
    subscription.record_payment(failed_payment) # 2nd

    # Act
    subscription.record_payment(failed_payment) # 3rd

    # Assert
    assert subscription.payment_failures == 3
    assert subscription.status == "SUSPENDED"

def test_br04_success_resets_failure_counter_from_active_state(subscription, failed_payment, success_payment):
    # BR04 - A successful payment must reset the consecutive payment failure counter to zero
    
    # Arrange
    subscription.record_payment(failed_payment)
    subscription.record_payment(failed_payment)
    assert subscription.payment_failures == 2

    # Act
    subscription.record_payment(success_payment)

    # Assert
    assert subscription.payment_failures == 0
    assert subscription.status == "ACTIVE"

def test_br04_success_resets_failure_counter_and_reactivates_from_suspended(subscription, failed_payment, success_payment):
    # BR04 - A successful payment must reset the consecutive payment failure counter to zero
    # FR02 - The system must update the subscription status
    
    # Arrange
    subscription.status = "SUSPENDED"
    subscription.payment_failures = 3

    # Act
    subscription.record_payment(success_payment)

    # Assert
    assert subscription.payment_failures == 0
    assert subscription.status == "ACTIVE"

def test_br02_canceled_subscription_cannot_be_reactivated_with_success_payment(subscription, success_payment):
    # BR02 - Subscriptions with status CANCELED must not be reactivated under any circumstances
    # FR04 - The system must prevent invalid state transitions
    # FR05 - The system must raise an exception in case of a failure (interpreted as operation failure)
    
    # Arrange
    subscription.status = "CANCELED"

    # Act / Assert
    with pytest.raises(Exception):
        subscription.record_payment(success_payment)

    # Post-condition Check: Status must remain CANCELED
    assert subscription.status == "CANCELED"

def test_br02_canceled_subscription_remains_canceled_on_failure(subscription, failed_payment):
    # BR02 - Subscriptions with status CANCELED must not be reactivated under any circumstances
    # FR04 - The system must prevent invalid state transitions
    # FR05 - The system must raise an exception in case of a failure
    
    # Arrange
    subscription.status = "CANCELED"

    # Act / Assert
    with pytest.raises(Exception):
        subscription.record_payment(failed_payment)

    # Post-condition Check: Status must remain CANCELED
    assert subscription.status == "CANCELED"

def test_br01_validate_initial_valid_state(subscription):
    # BR01 - A subscription may be in only one of the following states: ACTIVE...
    
    # Assert
    assert subscription.status in ["ACTIVE", "SUSPENDED", "CANCELED"]

# Note regarding BR05 (Billing dates must not be retroactive):
# Based strictly on the provided Class Diagram (UML) and System Context, 
# neither the Payment class nor the Subscription class contains date attributes 
# or methods accepting dates. To strictly adhere to General Constraint #1 
# ("Do not create rules... or behaviors that are not explicitly described"),
# a test for BR05 cannot be generated without fabricating attributes not present in the specification.
