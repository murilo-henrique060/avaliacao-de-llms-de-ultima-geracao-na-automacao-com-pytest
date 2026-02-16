import pytest

# NOTE:
# - These tests assume the SUT provides `Payment` and `Subscription` classes as specified.
# - Update the import path below to match your project structure.
from cases.case03 import Payment, Subscription  # noqa: F401


# -------------------------
# BR01: Allowed states only
# -------------------------

def test_br01_subscription_status_allows_active_state():
    # BR01 – A subscription may be in only one of: ACTIVE, SUSPENDED, CANCELED
    s = Subscription(status="ACTIVE", payment_failures=0)
    assert s.status == "ACTIVE"


def test_br01_subscription_status_allows_suspended_state():
    # BR01 – A subscription may be in only one of: ACTIVE, SUSPENDED, CANCELED
    s = Subscription(status="SUSPENDED", payment_failures=0)
    assert s.status == "SUSPENDED"


def test_br01_subscription_status_allows_canceled_state():
    # BR01 – A subscription may be in only one of: ACTIVE, SUSPENDED, CANCELED
    s = Subscription(status="CANCELED", payment_failures=0)
    assert s.status == "CANCELED"


def test_br01_subscription_status_rejects_any_other_state_by_exception():
    # BR01 – A subscription may be in only one of: ACTIVE, SUSPENDED, CANCELED
    # FR05 – The system must raise an exception in case of a failure
    with pytest.raises(Exception):
        Subscription(status="PAUSED", payment_failures=0)


# ----------------------------------------
# BR02: CANCELED must not be reactivated
# ----------------------------------------

def test_br02_canceled_subscription_must_not_be_reactivated_on_successful_payment():
    # BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
    # FR04 – The system must prevent invalid state transitions
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="CANCELED", payment_failures=0)
    p = Payment(success=True)

    with pytest.raises(Exception):
        s.record_payment(p)


# ---------------------------------------------------------
# BR03: Suspend after exactly 3 consecutive payment failures
# ---------------------------------------------------------

def test_br03_subscription_not_suspended_after_2_consecutive_failures():
    # BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 1
    assert s.status == "ACTIVE"

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 2
    assert s.status == "ACTIVE"


def test_br03_subscription_suspended_after_exactly_3_consecutive_failures():
    # BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 1
    assert s.status == "ACTIVE"

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 2
    assert s.status == "ACTIVE"

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 3
    assert s.status == "SUSPENDED"


# ---------------------------------------------------
# BR04: Success resets consecutive failures to zero
# ---------------------------------------------------

def test_br04_successful_payment_resets_failure_counter_to_zero():
    # BR04 – A successful payment must reset the consecutive payment failure counter to zero
    s = Subscription(status="ACTIVE", payment_failures=2)

    s.record_payment(Payment(success=True))
    assert s.payment_failures == 0


# ------------------------------------
# BR05: Billing dates not retroactive
# ------------------------------------
# The provided UML/specification includes no billing date attribute, parameter,
# or method input/output related to billing dates. Therefore, BR05 cannot be
# tested without inventing API or behavior, which is prohibited by constraints.


# -----------------------------
# FR01: The system must record payments
# -----------------------------

def test_fr01_record_payment_returns_a_value_on_success():
    # FR01 – The system must record payments
    s = Subscription(status="ACTIVE", payment_failures=0)

    result = s.record_payment(Payment(success=True))
    assert result is not None


# -------------------------------------------------------------
# FR02: Update subscription status based on payment success/failure
# -------------------------------------------------------------

def test_fr02_failure_payment_does_not_set_status_to_active_implicitly():
    # FR02 – The system must update the subscription status based on payment success or failure
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))

    # Only assert what is explicitly required: failure is recorded via the counter,
    # not any unstated state transitions.
    assert s.payment_failures == 1


def test_fr02_third_consecutive_failure_updates_status_to_suspended():
    # FR02 – The system must update the subscription status based on payment success or failure
    s = Subscription(status="ACTIVE", payment_failures=2)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))

    assert s.status == "SUSPENDED"


# ---------------------------------------------------
# FR03: Control number of consecutive payment failures
# ---------------------------------------------------

def test_fr03_each_failed_payment_increments_consecutive_failure_counter_by_one():
    # FR03 – The system must control the number of consecutive payment failures
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))

    assert s.payment_failures == 1


def test_fr03_successful_payment_resets_consecutive_failure_counter_to_zero():
    # FR03 – The system must control the number of consecutive payment failures
    s = Subscription(status="ACTIVE", payment_failures=1)

    s.record_payment(Payment(success=True))
    assert s.payment_failures == 0


# ------------------------------------------
# FR04: Prevent invalid state transitions
# ------------------------------------------

def test_fr04_prevent_invalid_transition_from_canceled_by_raising_exception():
    # FR04 – The system must prevent invalid state transitions
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="CANCELED", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=True))


# ------------------------------------------
# FR05: Raise an exception in case of a failure
# ------------------------------------------

def test_fr05_record_payment_raises_exception_when_payment_fails():
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))