import decimal
import pytest
from types import SimpleNamespace

# The system under test is expected to provide Subscription and Payment classes
# with the interfaces described in the specification.
from cases.case03 import Subscription, Payment


# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_subscription_status_is_one_of_allowed_values_after_initialization():
    subscription = Subscription()
    assert subscription.status in {"ACTIVE", "SUSPENDED", "CANCELED"}


# FR01 – The system must record payments
def test_fr01_record_payment_returns_decimal_amount_on_successful_payment():
    subscription = Subscription()
    payment = Payment(success=True)
    result = subscription.record_payment(payment)
    assert isinstance(result, decimal.Decimal)


# BR03 – Suspension after 3 consecutive payment failures (positive case)
def test_br03_subscription_suspended_after_third_consecutive_failure():
    subscription = Subscription()
    # perform three consecutive failing payments
    subscription.record_payment(Payment(success=False))
    subscription.record_payment(Payment(success=False))
    subscription.record_payment(Payment(success=False))
    assert subscription.status == "SUSPENDED"


# BR03 – Suspension after 3 consecutive payment failures (negative case: after two failures not suspended)
def test_br03_not_suspended_after_two_consecutive_failures():
    subscription = Subscription()
    subscription.record_payment(Payment(success=False))
    subscription.record_payment(Payment(success=False))
    assert subscription.status != "SUSPENDED"


# FR03 – The system must control the number of consecutive payment failures
def test_fr03_consecutive_failure_counter_increments_on_failure():
    subscription = Subscription()
    subscription.record_payment(Payment(success=False))
    assert subscription.payment_failures == 1


# FR04 – A successful payment must reset the consecutive payment failure counter to zero
def test_fr04_successful_payment_resets_consecutive_failure_counter():
    subscription = Subscription()
    subscription.record_payment(Payment(success=False))
    subscription.record_payment(Payment(success=False))
    # now a successful payment should reset the counter to zero
    subscription.record_payment(Payment(success=True))
    assert subscription.payment_failures == 0


# FR02 – The system must update the subscription status based on payment success
def test_fr02_successful_payment_updates_status_to_active():
    subscription = Subscription()
    # ensure starting from a non-active state to validate update to ACTIVE
    # if implementation allows direct assignment for test setup:
    subscription.status = "SUSPENDED"
    subscription.record_payment(Payment(success=True))
    assert subscription.status == "ACTIVE"


# BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
def test_br02_canceled_subscription_cannot_be_reactivated_raises_exception():
    subscription = Subscription()
    subscription.status = "CANCELED"
    # Attempting to record a successful payment on a canceled subscription must be prevented.
    # The test validates that the operation raises an exception (prevents reactivation).
    with pytest.raises(Exception):
        subscription.record_payment(Payment(success=True))


# FR05 – The system must raise an exception in case of a failure
def test_fr05_record_payment_with_invalid_payment_object_raises_exception():
    subscription = Subscription()
    # Provide an invalid payment object (missing 'success' attribute) to simulate input failure.
    invalid_payment = SimpleNamespace()  # no 'success' attribute
    with pytest.raises(Exception):
        subscription.record_payment(invalid_payment)


# BR05 – Billing dates must not be retroactive
def test_br05_record_payment_with_retroactive_billing_date_raises_exception():
    subscription = Subscription()
    # Use a payment-like object containing a retroactive billing date attribute.
    # The test validates the system rejects retroactive billing dates by raising an exception.
    # For determinism, use explicit dates as strings.
    retroactive_payment = SimpleNamespace(success=True, billing_date="2000-01-01")
    with pytest.raises(Exception):
        subscription.record_payment(retroactive_payment)