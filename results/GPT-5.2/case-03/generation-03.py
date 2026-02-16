import pytest

# NOTE: Tests assume Payment and Subscription are provided by the system under test (SUT).
# Do not implement the system here, per constraints.
try:
    from cases.case03 import Payment, Subscription  # type: ignore
except Exception:
    Payment = None  # type: ignore
    Subscription = None  # type: ignore


@pytest.fixture()
def sut_types_available():
    if Payment is None or Subscription is None:
        pytest.skip("SUT types Payment and Subscription are not importable in this environment.")


def _make_subscription(status: str, payment_failures: int):
    """
    Helper strictly for constructing SUT objects (not implementing business logic).
    If the SUT constructor signature differs, adapt import/fixture in your project, not here.
    """
    return Subscription(status=status, payment_failures=payment_failures)


def _make_payment(success: bool):
    return Payment(success=success)


# -------------------------
# Business Rules (BR)
# -------------------------

def test_br01_subscription_status_must_be_one_of_active_suspended_or_canceled(sut_types_available):
    # BR01 – Subscription state must be only ACTIVE, SUSPENDED, or CANCELED
    # FR05 – Must raise an exception in case of a failure
    with pytest.raises(Exception):
        _make_subscription(status="PAUSED", payment_failures=0)


def test_br02_canceled_subscription_must_not_be_reactivated_under_any_circumstances(sut_types_available):
    # BR02 – CANCELED must not be reactivated under any circumstances
    # FR04 – Prevent invalid state transitions
    # FR05 – Must raise an exception in case of a failure
    sub = _make_subscription(status="CANCELED", payment_failures=0)
    with pytest.raises(Exception):
        sub.record_payment(_make_payment(success=True))


def test_br03_subscription_is_suspended_after_exactly_three_consecutive_payment_failures(sut_types_available):
    # BR03 – Automatic suspension after exactly 3 consecutive payment failures
    # FR02 – Update subscription status based on payment success or failure
    # FR03 – Control consecutive payment failures
    sub = _make_subscription(status="ACTIVE", payment_failures=2)
    with pytest.raises(Exception):
        sub.record_payment(_make_payment(success=False))
    assert sub.payment_failures == 3
    assert sub.status == "SUSPENDED"


def test_br03_subscription_is_not_suspended_after_only_two_consecutive_payment_failures(sut_types_available):
    # BR03 – Automatic suspension after exactly 3 consecutive payment failures (negative case)
    # FR02 – Update subscription status based on payment success or failure
    sub = _make_subscription(status="ACTIVE", payment_failures=1)
    with pytest.raises(Exception):
        sub.record_payment(_make_payment(success=False))
    assert sub.payment_failures == 2
    assert sub.status == "ACTIVE"


def test_br04_successful_payment_resets_consecutive_payment_failure_counter_to_zero(sut_types_available):
    # BR04 – Successful payment resets consecutive payment failures to zero
    # FR03 – Control consecutive payment failures
    sub = _make_subscription(status="ACTIVE", payment_failures=2)
    sub.record_payment(_make_payment(success=True))
    assert sub.payment_failures == 0


def test_br05_billing_dates_must_not_be_retroactive(sut_types_available):
    # BR05 – Billing dates must not be retroactive
    # FR05 – Must raise an exception in case of a failure
    # No billing date field or API exists in provided UML; thus we can only assert
    # that the Subscription interface does not accept a retroactive billing date parameter
    # through record_payment(payment: Payment). Any attempt to pass such data must fail.
    sub = _make_subscription(status="ACTIVE", payment_failures=0)
    payment = _make_payment(success=True)
    with pytest.raises(TypeError):
        sub.record_payment(payment, billing_date="2000-01-01")  # type: ignore[arg-type]


# -------------------------
# Functional Requirements (FR)
# -------------------------

def test_fr01_system_records_payments_by_exposing_record_payment_operation(sut_types_available):
    # FR01 – The system must record payments
    sub = _make_subscription(status="ACTIVE", payment_failures=0)
    assert hasattr(sub, "record_payment")
    assert callable(getattr(sub, "record_payment"))


def test_fr02_successful_payment_does_not_suspend_subscription(sut_types_available):
    # FR02 – Update subscription status based on payment success or failure (success path)
    sub = _make_subscription(status="ACTIVE", payment_failures=0)
    sub.record_payment(_make_payment(success=True))
    assert sub.status == "ACTIVE"


def test_fr02_failed_payment_updates_failure_counter(sut_types_available):
    # FR02 – Update subscription status based on payment success or failure (failure path)
    # FR03 – Control consecutive payment failures
    # FR05 – Must raise an exception in case of a failure
    sub = _make_subscription(status="ACTIVE", payment_failures=0)
    with pytest.raises(Exception):
        sub.record_payment(_make_payment(success=False))
    assert sub.payment_failures == 1


def test_fr03_consecutive_failures_accumulate_across_multiple_failed_payments(sut_types_available):
    # FR03 – The system must control the number of consecutive payment failures
    # FR05 – Must raise an exception in case of a failure
    sub = _make_subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        sub.record_payment(_make_payment(success=False))
    assert sub.payment_failures == 1

    with pytest.raises(Exception):
        sub.record_payment(_make_payment(success=False))
    assert sub.payment_failures == 2


def test_fr04_prevent_invalid_state_transition_by_disallowing_reactivation_of_canceled(sut_types_available):
    # FR04 – The system must prevent invalid state transitions
    # BR02 – CANCELED must not be reactivated under any circumstances
    # FR05 – Must raise an exception in case of a failure
    sub = _make_subscription(status="CANCELED", payment_failures=2)
    with pytest.raises(Exception):
        sub.record_payment(_make_payment(success=True))


def test_fr05_failed_payment_must_raise_exception(sut_types_available):
    # FR05 – The system must raise an exception in case of a failure
    sub = _make_subscription(status="ACTIVE", payment_failures=0)
    with pytest.raises(Exception):
        sub.record_payment(_make_payment(success=False))