import pytest
from decimal import Decimal
from datetime import date

# The tests below assume the presence of the following classes and interface, as specified:
# - Payment with attribute `success: bool` (and optionally `billing_date` for BR05 test)
# - Subscription with attributes `status: str`, `payment_failures: int`, and method `record_payment(payment: Payment) -> Decimal`
#
# Tests exercise only behaviors explicitly described in the specification.

# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_subscription_status_is_one_of_allowed_states():
    # BR01
    # This test asserts that a Subscription instance's `status` is one of the allowed exact strings.
    from cases.case03 import Subscription

    sub = Subscription()
    assert sub.status in ("ACTIVE", "SUSPENDED", "CANCELED")


# BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
def test_br02_canceled_subscription_recording_successful_payment_raises_exception_and_remains_canceled():
    # BR02
    # Attempting to record a successful payment on a CANCELED subscription must not reactivate it;
    # the system MUST raise an exception to prevent reactivation.
    from subscription import Subscription, Payment

    sub = Subscription()
    sub.status = "CANCELED"
    payment = Payment(success=True)

    with pytest.raises(Exception):
        sub.record_payment(payment)

    assert sub.status == "CANCELED"


# BR03 – Suspension after 3 consecutive payment failures
def test_br03_subscription_automatically_suspends_after_exactly_three_consecutive_failures():
    # BR03
    # Three consecutive failed payments must result in status "SUSPENDED" and payment_failures == 3.
    from subscription import Subscription, Payment

    sub = Subscription()
    assert sub.payment_failures == 0

    for _ in range(3):
        with pytest.raises(Exception):
            sub.record_payment(Payment(success=False))

    assert sub.payment_failures == 3
    assert sub.status == "SUSPENDED"


# BR04 – A successful payment must reset the consecutive payment failure counter to zero
def test_br04_successful_payment_resets_consecutive_failure_counter_to_zero():
    # BR04
    # After one or more failures, a successful payment must set payment_failures to exactly 0.
    from subscription import Subscription, Payment
    from decimal import Decimal

    sub = Subscription()

    # produce two consecutive failures
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))

    assert sub.payment_failures == 2

    # successful payment should not raise and must reset counter to zero
    result = sub.record_payment(Payment(success=True))
    assert isinstance(result, Decimal)
    assert sub.payment_failures == 0


# BR05 – Billing dates must not be retroactive
def test_br05_reject_payment_with_billing_date_before_last_billing_date():
    # BR05
    # The system must prevent retroactive billing dates. If a Payment carries a billing_date earlier than
    # subscription.last_billing_date the system must raise an exception.
    from subscription import Subscription, Payment

    sub = Subscription()
    # Set a last_billing_date explicitly (attribute required by BR05)
    sub.last_billing_date = date(2026, 1, 10)

    retro_payment = Payment(success=True)
    # attach a billing_date earlier than last_billing_date
    retro_payment.billing_date = date(2026, 1, 9)

    with pytest.raises(Exception):
        sub.record_payment(retro_payment)

    # Ensure no change to last_billing_date occurred
    assert sub.last_billing_date == date(2026, 1, 10)


# FR01 – The system must record payments
def test_fr01_record_payment_returns_decimal_for_successful_payment():
    # FR01
    # record_payment must return a Decimal when a payment is successfully recorded.
    from subscription import Subscription, Payment
    from decimal import Decimal

    sub = Subscription()
    result = sub.record_payment(Payment(success=True))
    assert isinstance(result, Decimal)


# FR02 – The system must update the subscription status based on payment success or failure
def test_fr02_failed_payment_increments_failure_and_keeps_status_until_threshold():
    # FR02
    # A failed payment must update the subscription's failure counter by exactly +1 and must not
    # change the status before the suspension threshold is reached.
    from subscription import Subscription, Payment

    sub = Subscription()
    initial_status = sub.status
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))

    assert sub.payment_failures == 1
    assert sub.status == initial_status


# FR03 – The system must control the number of consecutive payment failures
def test_fr03_consecutive_failures_increment_counter_precisely():
    # FR03
    # Each failed payment must increment payment_failures by exactly one (deterministic).
    from subscription import Subscription, Payment

    sub = Subscription()
    assert sub.payment_failures == 0

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 1

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 2


# FR04 – The system must prevent invalid state transitions
def test_fr04_prevent_reactivation_of_canceled_subscription_via_payment_attempt_raises_exception():
    # FR04
    # The system must prevent invalid state transitions; attempting to transition from CANCELED to ACTIVE
    # by recording a successful payment must raise an exception.
    from subscription import Subscription, Payment

    sub = Subscription()
    sub.status = "CANCELED"

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=True))

    # Confirm state unchanged
    assert sub.status == "CANCELED"


# FR05 – The system must raise an exception in case of a failure
def test_fr05_recording_failed_payment_raises_exception():
    # FR05
    # Recording a failed payment must raise an exception (validation failure).
    from subscription import Subscription, Payment

    sub = Subscription()

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))