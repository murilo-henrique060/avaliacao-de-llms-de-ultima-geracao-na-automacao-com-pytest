import pytest

# NOTE:
# These tests assume the SUT provides `Subscription` and `Payment` classes matching the UML.
# They intentionally do NOT implement the system.
from cases.case03 import Subscription, Payment  # type: ignore


def test_br01_allows_only_active_status_string():
    # BR01 – Only allowed states: ACTIVE, SUSPENDED, CANCELED
    s = Subscription(status="ACTIVE", payment_failures=0)
    assert s.status == "ACTIVE"


def test_br01_allows_only_suspended_status_string():
    # BR01 – Only allowed states: ACTIVE, SUSPENDED, CANCELED
    s = Subscription(status="SUSPENDED", payment_failures=0)
    assert s.status == "SUSPENDED"


def test_br01_allows_only_canceled_status_string():
    # BR01 – Only allowed states: ACTIVE, SUSPENDED, CANCELED
    s = Subscription(status="CANCELED", payment_failures=0)
    assert s.status == "CANCELED"


def test_br01_rejects_unknown_status_string_with_exception():
    # BR01 – Only allowed states: ACTIVE, SUSPENDED, CANCELED
    with pytest.raises(Exception):
        Subscription(status="PAUSED", payment_failures=0)


def test_br02_canceled_subscription_must_not_be_reactivated_when_payment_succeeds():
    # BR02 – CANCELED must not be reactivated under any circumstances
    s = Subscription(status="CANCELED", payment_failures=0)
    p = Payment(success=True)

    with pytest.raises(Exception):
        s.record_payment(p)


def test_br03_suspends_after_exactly_three_consecutive_failures():
    # BR03 – Automatically suspended after exactly 3 consecutive payment failures
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.status == "ACTIVE"
    assert s.payment_failures == 1

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.status == "ACTIVE"
    assert s.payment_failures == 2

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.status == "SUSPENDED"
    assert s.payment_failures == 3


def test_br03_does_not_suspend_before_three_consecutive_failures():
    # BR03 – Automatically suspended after exactly 3 consecutive payment failures
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.status != "SUSPENDED"
    assert s.payment_failures == 1

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.status != "SUSPENDED"
    assert s.payment_failures == 2


def test_br04_successful_payment_resets_failure_counter_to_zero():
    # BR04 – Successful payment resets consecutive payment failure counter to zero
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 1

    # Successful payment must reset to zero
    s.record_payment(Payment(success=True))
    assert s.payment_failures == 0


def test_br04_successful_payment_resets_failure_counter_from_two_to_zero():
    # BR04 – Successful payment resets consecutive payment failure counter to zero
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 2

    s.record_payment(Payment(success=True))
    assert s.payment_failures == 0


def test_br05_billing_dates_must_not_be_retroactive_raises_exception():
    # BR05 – Billing dates must not be retroactive
    # No billing date attribute or API is defined in the UML; attempting to validate this rule
    # requires an explicit interface. This test enforces that retroactive billing cannot be
    # performed via `record_payment` if a date parameter is (incorrectly) accepted.
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(TypeError):
        s.record_payment(Payment(success=True), billing_date="2000-01-01")  # type: ignore[call-arg]


def test_fr01_system_records_payments_return_value_is_produced_on_success():
    # FR01 – The system must record payments
    s = Subscription(status="ACTIVE", payment_failures=0)
    result = s.record_payment(Payment(success=True))
    assert result is not None


def test_fr02_updates_subscription_status_to_suspended_after_three_failures():
    # FR02 – Update subscription status based on payment success or failure
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))

    assert s.status == "SUSPENDED"


def test_fr03_controls_consecutive_payment_failures_increments_on_each_failure():
    # FR03 – Control the number of consecutive payment failures
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 1

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 2


def test_fr04_prevents_invalid_state_transition_from_canceled_on_payment_attempt():
    # FR04 – Prevent invalid state transitions
    s = Subscription(status="CANCELED", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=True))


def test_fr05_raises_exception_in_case_of_payment_failure():
    # FR05 – Raise an exception in case of a failure
    s = Subscription(status="ACTIVE", payment_failures=0)
    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))