import pytest

# NOTE:
# These tests assume the SUT provides classes named Payment and Subscription
# with the interface defined in the provided UML (success attribute; status,
# payment_failures attributes; record_payment method).
#
# Adjust the import below to match the actual module/package name in your codebase.
from cases.case03 import Payment, Subscription  # noqa: F401


# -------------------------
# BR01 — Allowed statuses
# -------------------------

def test_br01_subscription_status_can_be_active():
    # BR01 – Allowed states: ACTIVE, SUSPENDED, CANCELED
    s = Subscription(status="ACTIVE", payment_failures=0)
    assert s.status == "ACTIVE"


def test_br01_subscription_status_can_be_suspended():
    # BR01 – Allowed states: ACTIVE, SUSPENDED, CANCELED
    s = Subscription(status="SUSPENDED", payment_failures=0)
    assert s.status == "SUSPENDED"


def test_br01_subscription_status_can_be_canceled():
    # BR01 – Allowed states: ACTIVE, SUSPENDED, CANCELED
    s = Subscription(status="CANCELED", payment_failures=0)
    assert s.status == "CANCELED"


def test_br01_subscription_status_rejects_state_outside_defined_set():
    # BR01 – Allowed states: ACTIVE, SUSPENDED, CANCELED
    # FR05 – The system must raise an exception in case of a failure
    with pytest.raises(Exception):
        Subscription(status="PAUSED", payment_failures=0)


# -----------------------------------------------
# BR02 — CANCELED must never be reactivated
# -----------------------------------------------

def test_br02_canceled_subscription_cannot_be_reactivated_by_successful_payment():
    # BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
    # FR04 – The system must prevent invalid state transitions
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="CANCELED", payment_failures=0)
    p = Payment(success=True)

    with pytest.raises(Exception):
        s.record_payment(p)


# --------------------------------------------------------
# BR03 — Auto-suspend after exactly 3 consecutive failures
# --------------------------------------------------------

def test_br03_suspended_after_exactly_three_consecutive_payment_failures():
    # BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
    # FR02 – The system must update the subscription status based on payment success or failure
    # FR03 – The system must control the number of consecutive payment failures
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


def test_br03_not_suspended_after_exactly_two_consecutive_payment_failures():
    # BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.status == "ACTIVE"
    assert s.payment_failures == 1

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.status == "ACTIVE"
    assert s.payment_failures == 2


# -------------------------------------------------------
# BR04 — Successful payment resets failure counter to zero
# -------------------------------------------------------

def test_br04_successful_payment_resets_consecutive_failure_counter_to_zero():
    # BR04 – A successful payment must reset the consecutive payment failure counter to zero
    # FR03 – The system must control the number of consecutive payment failures
    s = Subscription(status="ACTIVE", payment_failures=2)

    s.record_payment(Payment(success=True))

    assert s.payment_failures == 0


def test_br04_successful_payment_resets_failure_counter_even_after_one_failure_exception():
    # BR04 – A successful payment must reset the consecutive payment failure counter to zero
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 1

    s.record_payment(Payment(success=True))
    assert s.payment_failures == 0


# -----------------------------------
# BR05 — Billing dates not retroactive
# -----------------------------------
# NOTE:
# The provided UML and requirements do not define any billing date field, input,
# or API surface for setting/validating billing dates. Therefore, no test can be
# written without inventing behavior or interfaces, which is forbidden by the
# constraints.


# -------------------------
# FR01 — Record payments
# -------------------------

def test_fr01_record_payment_records_successful_payment_without_exception():
    # FR01 – The system must record payments
    s = Subscription(status="ACTIVE", payment_failures=0)

    s.record_payment(Payment(success=True))


def test_fr01_record_payment_records_failed_payment_by_raising_exception():
    # FR01 – The system must record payments
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))


# ---------------------------------------------------------
# FR02 — Update status based on payment success or failure
# ---------------------------------------------------------

def test_fr02_failed_payment_increments_failures_without_changing_status_before_threshold():
    # FR02 – The system must update the subscription status based on payment success or failure
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))

    assert s.status == "ACTIVE"
    assert s.payment_failures == 1


def test_fr02_third_consecutive_failed_payment_updates_status_to_suspended():
    # FR02 – The system must update the subscription status based on payment success or failure
    s = Subscription(status="ACTIVE", payment_failures=2)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))

    assert s.status == "SUSPENDED"
    assert s.payment_failures == 3


# -----------------------------------------------
# FR03 — Control consecutive payment failure count
# -----------------------------------------------

def test_fr03_failure_counter_increments_by_one_on_each_failed_payment():
    # FR03 – The system must control the number of consecutive payment failures
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 1

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))
    assert s.payment_failures == 2


def test_fr03_failure_counter_resets_to_zero_on_successful_payment():
    # FR03 – The system must control the number of consecutive payment failures
    s = Subscription(status="ACTIVE", payment_failures=1)

    s.record_payment(Payment(success=True))

    assert s.payment_failures == 0


# --------------------------------------------
# FR04 — Prevent invalid state transitions
# --------------------------------------------

def test_fr04_prevent_invalid_transition_from_canceled_via_record_payment():
    # FR04 – The system must prevent invalid state transitions
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="CANCELED", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=True))


# -----------------------------------------
# FR05 — Raise an exception in case of failure
# -----------------------------------------

def test_fr05_failed_payment_raises_exception():
    # FR05 – The system must raise an exception in case of a failure
    s = Subscription(status="ACTIVE", payment_failures=0)

    with pytest.raises(Exception):
        s.record_payment(Payment(success=False))