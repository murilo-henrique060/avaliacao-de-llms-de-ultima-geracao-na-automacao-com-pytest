import datetime
from decimal import Decimal
import pytest

# The tests below assume the presence of a module `subscription` that provides
# Subscription and Payment classes as per the provided specification:
# - Payment(success: bool[, billing_date: date])
# - Subscription with attributes:
#     - status: "ACTIVE" | "SUSPENDED" | "CANCELED"
#     - payment_failures: int
#     - record_payment(payment: Payment) -> Decimal
#
# Tests validate behaviors described in BR and FR. They do not implement system logic.

from cases.case03 import Subscription, Payment


# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_allows_initializing_with_status_active():
    # BR01 – validate correct behavior for allowed state "ACTIVE"
    sub = Subscription(status="ACTIVE", payment_failures=0)
    assert sub.status == "ACTIVE"


def test_br01_rejects_invalid_status_value_on_initialization():
    # BR01 – expose violation when attempting to use an invalid state value
    with pytest.raises(ValueError):
        Subscription(status="PAUSED", payment_failures=0)


# BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
def test_br02_canceled_subscription_cannot_be_reactivated_via_successful_payment():
    # BR02 – attempting to reactivate a CANCELED subscription via record_payment must be prevented
    sub = Subscription(status="CANCELED", payment_failures=0)
    payment = Payment(success=True)
    with pytest.raises(Exception):
        sub.record_payment(payment)
    assert sub.status == "CANCELED"


# BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
def test_br03_suspends_after_exactly_three_consecutive_payment_failures():
    # BR03 – after exactly three consecutive failures subscription becomes SUSPENDED
    sub = Subscription(status="ACTIVE", payment_failures=0)
    # First failure
    sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 1
    assert sub.status == "ACTIVE"
    # Second failure
    sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 2
    assert sub.status == "ACTIVE"
    # Third failure -> suspension exactly at 3
    sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 3
    assert sub.status == "SUSPENDED"


# BR04 – A successful payment must reset the consecutive payment failure counter to zero
def test_br04_successful_payment_resets_failure_counter_to_zero():
    # BR04 – a single successful payment resets payment_failures to 0
    sub = Subscription(status="ACTIVE", payment_failures=2)
    sub.record_payment(Payment(success=True))
    assert sub.payment_failures == 0


# BR05 – Billing dates must not be retroactive
def test_br05_rejects_retroactive_billing_dates():
    # BR05 – recording a payment with a billing_date earlier than a previously recorded billing_date must be rejected
    sub = Subscription(status="ACTIVE", payment_failures=0)
    first_date = datetime.date(2026, 1, 10)
    sub.record_payment(Payment(success=True, billing_date=first_date))
    assert sub.payment_failures == 0
    # Attempt retroactive billing date
    retro_date = datetime.date(2026, 1, 9)
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=True, billing_date=retro_date))
    # Ensure state and failure counter unchanged after rejected retroactive attempt
    assert sub.status == "ACTIVE"
    assert sub.payment_failures == 0


# FR01 – The system must record payments
def test_fr01_record_payment_returns_decimal_instance():
    # FR01 – record_payment must return a Decimal indicating recording success/output type
    sub = Subscription(status="ACTIVE", payment_failures=0)
    result = sub.record_payment(Payment(success=True))
    assert isinstance(result, Decimal)


# FR02 – The system must update the subscription status based on payment success or failure
def test_fr02_failed_payment_increments_failure_counter_and_keeps_status_active_until_threshold():
    # FR02 – a failed payment increments payment_failures by exactly one and does not change status before threshold
    sub = Subscription(status="ACTIVE", payment_failures=0)
    sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 1
    assert sub.status == "ACTIVE"


# FR03 – The system must control the number of consecutive payment failures
def test_fr03_each_consecutive_failure_increments_counter_by_one():
    # FR03 – each failure increments payment_failures by exactly 1
    sub = Subscription(status="ACTIVE", payment_failures=0)
    sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 1
    sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 2


# FR04 – The system must prevent invalid state transitions
def test_fr04_prevent_direct_status_change_from_canceled_to_active_raises_exception():
    # FR04 – preventing invalid state transition via direct status assignment or equivalent API must raise
    sub = Subscription(status="CANCELED", payment_failures=0)
    with pytest.raises(Exception):
        # Attempt to force a transition; this may be via setter or dedicated method in implementation
        sub.status = "ACTIVE"


# FR05 – The system must raise an exception in case of a failure
def test_fr05_recording_payment_with_retroactive_billing_date_raises_exception():
    # FR05 – in case of an invalid operation (retroactive billing date) the system raises an exception
    sub = Subscription(status="ACTIVE", payment_failures=0)
    valid_date = datetime.date(2026, 1, 15)
    sub.record_payment(Payment(success=True, billing_date=valid_date))
    invalid_date = datetime.date(2026, 1, 14)
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=True, billing_date=invalid_date))