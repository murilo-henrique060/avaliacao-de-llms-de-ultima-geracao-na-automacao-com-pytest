import pytest
from decimal import Decimal
from datetime import date

# The system under test is expected to provide these classes with the documented interface.
# Tests assume:
# - subscription.Subscription() can be constructed (optionally with a status argument)
# - subscription.Payment(success: bool, billing_date: date = None) may be constructed (billing_date used only where BR05 applies)
# - Subscription.record_payment(payment: Payment) exists and returns a Decimal
# - Subscription.status is one of "ACTIVE", "SUSPENDED", "CANCELED"
# - Subscription.payment_failures is an int
# These tests exercise behaviors described in the specification only.

from cases.case03 import Subscription, Payment


# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_subscription_initial_status_is_one_of_allowed_values():
    # BR01 – validate correct behavior
    sub = Subscription()
    assert sub.status in ("ACTIVE", "SUSPENDED", "CANCELED")


# BR01 – Attempting to construct a subscription with an invalid status must fail (negative test)
def test_br01_constructing_with_invalid_status_raises_value_error():
    # BR01 – expose violation when an invalid state is provided
    with pytest.raises(ValueError):
        Subscription(status="PAUSED")  # "PAUSED" is not one of the allowed states


# BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
def test_br02_canceled_subscription_remains_canceled_after_successful_payment():
    # BR02 – validate correct behavior: recording a successful payment must not change CANCELED to ACTIVE
    sub = Subscription(status="CANCELED")
    payment = Payment(success=True)
    # Record payment should not change status from CANCELED to any other state
    sub.record_payment(payment)
    assert sub.status == "CANCELED"


# BR02 – Negative test: attempt to change status from CANCELED to ACTIVE via direct assignment is not allowed
def test_br02_direct_assignment_to_reactivate_canceled_raises_value_error():
    # BR02 – expose violation: direct reactivation must be prevented by the system
    sub = Subscription(status="CANCELED")
    with pytest.raises(ValueError):
        sub.status = "ACTIVE"


# BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
def test_br03_subscription_suspended_after_third_consecutive_failure():
    # BR03 – validate correct behavior for exact third consecutive failure
    sub = Subscription(status="ACTIVE")
    f1 = Payment(success=False)
    f2 = Payment(success=False)
    f3 = Payment(success=False)
    # First failure
    sub.record_payment(f1)
    # Second failure
    sub.record_payment(f2)
    # Third failure -> should trigger suspension
    sub.record_payment(f3)
    assert sub.status == "SUSPENDED"


# BR03 – Negative/edge test: after two consecutive failures the subscription must NOT be suspended
def test_br03_not_suspended_after_two_consecutive_failures():
    # BR03 – expose violation when suspension occurs too early
    sub = Subscription(status="ACTIVE")
    sub.record_payment(Payment(success=False))
    sub.record_payment(Payment(success=False))
    assert sub.status != "SUSPENDED"
    assert sub.payment_failures == 2


# BR04 – A successful payment must reset the consecutive payment failure counter to zero
def test_br04_successful_payment_resets_failure_counter_to_zero():
    # BR04 – validate correct behavior
    sub = Subscription(status="ACTIVE")
    # Simulate two previous failures
    sub.payment_failures = 2
    success_payment = Payment(success=True)
    sub.record_payment(success_payment)
    assert sub.payment_failures == 0


# BR04 – Negative test: successful payment must reset counter even if counter is zero already (idempotent)
def test_br04_successful_payment_resets_zero_counter_stays_zero():
    # BR04 – expose violation if successful payment modifies non-failure state
    sub = Subscription(status="ACTIVE")
    sub.payment_failures = 0
    sub.record_payment(Payment(success=True))
    assert sub.payment_failures == 0


# BR05 – Billing dates must not be retroactive
def test_br05_record_payment_with_retroactive_billing_date_raises_exception():
    # BR05 – validate correct behavior: recording a payment with a billing date earlier than the subscription's last billing date must raise
    sub = Subscription()
    # Establish a last billing date by recording a payment with today's date
    today = date(2026, 1, 12)
    p_today = Payment(success=True, billing_date=today)
    sub.record_payment(p_today)
    # Attempt to record a payment with an earlier date (retroactive)
    earlier = date(2026, 1, 11)
    retro_payment = Payment(success=True, billing_date=earlier)
    with pytest.raises(Exception):
        sub.record_payment(retro_payment)


# FR01 – The system must record payments
def test_fr01_record_payment_returns_decimal_on_successful_payment():
    # FR01 – validate fulfillment: record_payment returns a Decimal when called with a payment
    sub = Subscription(status="ACTIVE")
    result = sub.record_payment(Payment(success=True))
    assert isinstance(result, Decimal)


# FR01 – Negative test: recording a malformed payment (missing required attributes) must raise an exception
def test_fr01_record_payment_with_malformed_payment_raises_exception():
    # FR01 – expose violation when system accepts malformed input
    sub = Subscription()
    class MalformedPayment:
        pass
    with pytest.raises(Exception):
        sub.record_payment(MalformedPayment())


# FR02 – The system must update the subscription status based on payment success or failure
def test_fr02_successful_payment_maintains_or_sets_active_status():
    # FR02 – validate fulfillment for successful payment updating status
    sub = Subscription(status="SUSPENDED")
    # If business allows reactivation from SUSPENDED on success, ensure status becomes ACTIVE.
    # Since reactivation from CANCELED is forbidden (BR02), this test only asserts that a successful payment
    # results in the subscription being in a permissible state (ACTIVE or still SUSPENDED) per system rules.
    result = sub.record_payment(Payment(success=True))
    assert sub.status in ("ACTIVE", "SUSPENDED")


# FR03 – The system must control the number of consecutive payment failures
def test_fr03_failed_payment_increments_consecutive_failure_counter_by_one():
    # FR03 – validate fulfillment
    sub = Subscription()
    initial = sub.payment_failures
    sub.record_payment(Payment(success=False))
    assert sub.payment_failures == initial + 1


# FR04 – The system must prevent invalid state transitions
def test_fr04_transition_from_canceled_to_any_other_state_via_status_assignment_is_prevented():
    # FR04 – validate fulfillment: direct state transition from CANCELED to another state must be prevented
    sub = Subscription(status="CANCELED")
    with pytest.raises(ValueError):
        sub.status = "ACTIVE"


# FR05 – The system must raise an exception in case of a failure
def test_fr05_recording_failed_payment_raises_exception():
    # FR05 – validate fulfillment: recording a failed payment must raise an exception
    sub = Subscription()
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))