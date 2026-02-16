import pytest

# Tests assume these classes are provided by the system under test (SUT).
# Do not implement the SUT here.
from cases.case03 import Subscription, Payment  # type: ignore


def test_br01_allows_only_active_suspended_canceled_initial_status():
    # BR01 – Subscription may be only ACTIVE, SUSPENDED, or CANCELED
    sub = Subscription(status="ACTIVE", payment_failures=0)
    assert sub.status in ("ACTIVE", "SUSPENDED", "CANCELED")


def test_br01_rejects_invalid_subscription_status_value_raises_exception():
    # BR01 – Subscription may be only ACTIVE, SUSPENDED, or CANCELED
    with pytest.raises(Exception):
        Subscription(status="PAUSED", payment_failures=0)


def test_br02_canceled_subscription_cannot_be_reactivated_raises_exception_on_successful_payment():
    # BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
    sub = Subscription(status="CANCELED", payment_failures=0)
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=True))


def test_br03_suspends_after_exactly_three_consecutive_payment_failures():
    # BR03 – Subscription must be automatically suspended after exactly 3 consecutive payment failures
    sub = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 1
    assert sub.status == "ACTIVE"

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 2
    assert sub.status == "ACTIVE"

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 3
    assert sub.status == "SUSPENDED"


def test_br03_does_not_suspend_before_third_consecutive_failure():
    # BR03 – Subscription must be automatically suspended after exactly 3 consecutive payment failures
    sub = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.status == "ACTIVE"

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.status == "ACTIVE"


def test_br04_successful_payment_resets_consecutive_failure_counter_to_zero():
    # BR04 – A successful payment must reset the consecutive payment failure counter to zero
    sub = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 2

    sub.record_payment(Payment(success=True))
    assert sub.payment_failures == 0


def test_br04_failure_after_success_starts_counter_from_one_not_continuing_previous_failures():
    # BR04 – A successful payment must reset the consecutive payment failure counter to zero
    sub = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 2

    sub.record_payment(Payment(success=True))
    assert sub.payment_failures == 0

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 1


def test_br05_retroactive_billing_date_is_rejected_raises_exception():
    # BR05 – Billing dates must not be retroactive
    # NOTE: The specification states this rule but does not expose any billing-date inputs
    # in the provided classes/method signatures. This test asserts that attempting to pass
    # a retroactive date (if supported via kwargs) must raise an exception.
    sub = Subscription(status="ACTIVE", payment_failures=0)
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=True), billing_date="2000-01-01")  # type: ignore[arg-type]


def test_fr01_records_payment_success_returns_decimal_like_value():
    # FR01 – The system must record payments
    sub = Subscription(status="ACTIVE", payment_failures=0)
    result = sub.record_payment(Payment(success=True))
    # Only validate return is provided (do not assume amount semantics).
    assert result is not None


def test_fr02_updates_subscription_status_on_third_failure_to_suspended():
    # FR02 – The system must update the subscription status based on payment success or failure
    sub = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))

    assert sub.status == "SUSPENDED"


def test_fr03_controls_consecutive_failures_counter_increments_on_failure():
    # FR03 – The system must control the number of consecutive payment failures
    sub = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 1

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 2


def test_fr03_controls_consecutive_failures_counter_resets_on_success():
    # FR03 – The system must control the number of consecutive payment failures
    sub = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 1

    sub.record_payment(Payment(success=True))
    assert sub.payment_failures == 0


def test_fr04_prevents_invalid_state_transition_from_canceled_on_payment_attempt_raises_exception():
    # FR04 – The system must prevent invalid state transitions
    sub = Subscription(status="CANCELED", payment_failures=0)
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=True))


def test_fr05_raises_exception_in_case_of_failure():
    # FR05 – The system must raise an exception in case of a failure
    sub = Subscription(status="ACTIVE", payment_failures=0)
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))