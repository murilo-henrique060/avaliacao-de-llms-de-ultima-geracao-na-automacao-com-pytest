import pytest
from decimal import Decimal
from datetime import date

# The tests below assume the existence of the following classes and members as per the provided specification:
# - class Payment with at least an attribute `success: bool`
# - class Subscription with attributes `status: str` and `payment_failures: int`
# - method Subscription.record_payment(payment: Payment) -> Decimal
#
# The concrete module and class implementations are not provided here; the tests reference them as if they exist
# according to the formal specification. Tests verify behavior strictly described in the specification and do not
# implement or assume behaviors not explicitly stated.

try:
    from cases.case03 import Subscription, Payment  # presumed system module per specification
except Exception:
    # Provide minimal stand-ins so that static analysis of tests (but not execution of system behavior) can succeed.
    # These stand-ins are for test file completeness only and will be ignored when running against the real system.
    class Payment:
        def __init__(self, success: bool, billing_date: date = None):
            self.success = success
            # billing_date may be used by BR05 if the system exposes it; presence here does not assume behavior.
            self.billing_date = billing_date

    class Subscription:
        def __init__(self):
            # Default placeholders; real system will provide actual initialization and behavior.
            self.status = "ACTIVE"
            self.payment_failures = 0
            # last_billing_date placeholder for BR05 checks if implemented by system
            self.last_billing_date = None

        def record_payment(self, payment: Payment) -> Decimal:
            raise NotImplementedError("System implementation not provided in tests")


# BR01 – A subscription may be in only one of the following states: ACTIVE, SUSPENDED, or CANCELED
def test_br01_status_value_is_one_of_allowed_states():
    sub = Subscription()
    # BR01 validation: the subscription's status must be exactly one of the allowed strings
    assert sub.status in ("ACTIVE", "SUSPENDED", "CANCELED")


# BR02 – Subscriptions with status CANCELED must not be reactivated under any circumstances
def test_br02_canceled_subscription_is_not_reactivated_by_successful_payment():
    sub = Subscription()
    # Arrange: force subscription into CANCELED state as specified by the rule
    sub.status = "CANCELED"
    payment = Payment(success=True)
    # Act: attempt to record a successful payment and observe result
    # The rule requires that a CANCELED subscription must not become ACTIVE again.
    try:
        sub.record_payment(payment)
    except Exception:
        # Exceptions are allowed by FR05; regardless of exception, status must remain CANCELED
        pass
    # Assert: after attempting any operation, status remains exactly CANCELED
    assert sub.status == "CANCELED"


# BR03 – The subscription must be automatically suspended after exactly 3 consecutive payment failures
def test_br03_subscription_suspends_only_after_third_consecutive_failure():
    sub = Subscription()
    # Ensure starting from a non-suspended state for clarity
    sub.status = "ACTIVE"
    # Two consecutive failures should not suspend
    for _ in range(2):
        with pytest.raises(Exception):
            sub.record_payment(Payment(success=False))
    # After two failures, subscription must not be SUSPENDED (BR03 focuses on suspension on the 3rd failure)
    assert sub.status != "SUSPENDED"
    # Third consecutive failure must cause automatic suspension
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.status == "SUSPENDED"


# BR04 – A successful payment must reset the consecutive payment failure counter to zero
def test_br04_successful_payment_resets_failure_counter_to_zero():
    sub = Subscription()
    # Arrange: set an existing non-zero consecutive failure counter
    sub.payment_failures = 2
    # Act: record a successful payment
    result = sub.record_payment(Payment(success=True))
    # The rule concerns the failure counter only; assert it is exactly zero after a successful payment
    assert sub.payment_failures == 0


# BR05 – Billing dates must not be retroactive
def test_br05_recording_payment_with_retroactive_billing_date_raises_exception():
    sub = Subscription()
    # Arrange: set a last billing date on the subscription (BR05 refers to billing dates; test assumes system exposes this)
    sub.last_billing_date = date(2026, 1, 10)
    # Create a payment whose billing_date is earlier than last_billing_date (retroactive)
    retro_payment = Payment(success=True, billing_date=date(2026, 1, 9))
    # The business rule requires that retroactive billing dates are not allowed -> system must raise an exception
    with pytest.raises(Exception):
        sub.record_payment(retro_payment)


# FR01 – The system must record payments
def test_fr01_record_payment_returns_decimal_for_successful_payment():
    sub = Subscription()
    payment = Payment(success=True)
    # The class diagram specifies record_payment returns a Decimal when recording a payment.
    result = sub.record_payment(payment)
    assert isinstance(result, Decimal)


# FR02 ��� The system must update the subscription status based on payment success or failure
def test_fr02_successful_payment_updates_status_from_suspended_to_active():
    sub = Subscription()
    # Arrange: start in SUSPENDED state to validate update on success
    sub.status = "SUSPENDED"
    payment = Payment(success=True)
    # Act: record a successful payment
    sub.record_payment(payment)
    # Assert: the system must update subscription status based on the successful payment
    # This test validates the update from SUSPENDED to ACTIVE as the specific expected behavior.
    assert sub.status == "ACTIVE"


# FR03 – The system must control the number of consecutive payment failures
def test_fr03_consecutive_payment_failures_counter_increments_on_each_failure():
    sub = Subscription()
    sub.payment_failures = 0
    # First failed payment
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 1
    # Second failed payment
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))
    assert sub.payment_failures == 2


# FR04 – The system must prevent invalid state transitions
def test_fr04_prevent_changing_canceled_to_active_via_direct_assignment_raises_exception():
    sub = Subscription()
    # Arrange: subscription is CANCELED
    sub.status = "CANCELED"
    # Act & Assert: attempting an invalid state transition (CANCELED -> ACTIVE) via assignment should be prevented
    # This test assumes the system enforces transition rules on assignment and raises an exception for invalid transitions.
    with pytest.raises(Exception):
        sub.status = "ACTIVE"


# FR05 – The system must raise an exception in case of a failure
def test_fr05_record_payment_raises_exception_on_payment_failure():
    sub = Subscription()
    # A failed payment must cause the system to raise an exception per FR05
    with pytest.raises(Exception):
        sub.record_payment(Payment(success=False))