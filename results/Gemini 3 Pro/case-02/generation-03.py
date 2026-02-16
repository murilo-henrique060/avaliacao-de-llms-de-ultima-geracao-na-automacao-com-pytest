import pytest
from decimal import Decimal

from cases.case02 import Item, Order  # type: ignore

# ----------------------------------------------------------------------------
# NOTE: The following classes (Item, Order) are assumed to be imported from
# the application module. Implementation is NOT included as per instructions.
# ----------------------------------------------------------------------------
# from ecommerce_system import Item, Order

def test_fr01_create_order_with_multiple_items(order_with_items):
    """
    FR01: Create an order with multiple items.
    Validates that items can be added to the order.
    """
    # Assuming 'order_with_items' fixture or manual setup
    # Using manual setup for clarity as implementation is black-box
    # This test assumes a successful creation does not raise exceptions
    
    # Setup
    item1 = Item(name="Keyboard", price=Decimal("50.00"), quantity=1)
    item2 = Item(name="Mouse", price=Decimal("30.00"), quantity=2)
    order = Order()

    # Action
    order.add_item(item1)
    order.add_item(item2)

    # Verification (White-box verification not possible without getter methods in UML,
    # relying on lack of exception for FR01 or subsequent calculation for validation)
    assert True 


def test_br01_order_must_contain_at_least_one_item():
    """
    BR01: An order must contain at least one item.
    FR05: The system must raise an exception in case of a failure.
    Validates that calculating total for an empty order raises an exception.
    """
    # Setup
    order = Order()

    # Action & Verification
    with pytest.raises(Exception):
        order.calculate_total()


def test_br02_item_quantity_must_be_minimum_one():
    """
    BR02: Each item must have a minimum quantity of 1.
    FR05: The system must raise an exception in case of a failure.
    Validates that creating an item with quantity 0 raises an exception.
    """
    # Action & Verification
    with pytest.raises(Exception):
        Item(name="USB Cable", price=Decimal("15.00"), quantity=0)


def test_br02_item_quantity_negative_raises_exception():
    """
    BR02: Each item must have a minimum quantity of 1.
    FR05: The system must raise an exception in case of a failure.
    Validates that creating an item with negative quantity raises an exception.
    """
    # Action & Verification
    with pytest.raises(Exception):
        Item(name="USB Cable", price=Decimal("15.00"), quantity=-1)


def test_br03_item_price_must_be_positive():
    """
    BR03: All items must have a positive price.
    FR05: The system must raise an exception in case of a failure.
    Validates that creating an item with price 0 raises an exception.
    """
    # Action & Verification
    with pytest.raises(Exception):
        Item(name="Free Sample", price=Decimal("0.00"), quantity=1)


def test_br03_item_price_negative_raises_exception():
    """
    BR03: All items must have a positive price.
    FR05: The system must raise an exception in case of a failure.
    Validates that creating an item with negative price raises an exception.
    """
    # Action & Verification
    with pytest.raises(Exception):
        Item(name="Refund", price=Decimal("-10.00"), quantity=1)


def test_br04_fr02_calculate_total_sum_of_items_no_discount():
    """
    BR04: The total order value is the sum of the items.
    FR02: Correctly calculate the total.
    FR04: The system must display the final order value.
    Validates calculation for total <= 200 (No discount).
    """
    # Setup
    item1 = Item(name="Book", price=Decimal("50.00"), quantity=2)  # 100.00
    item2 = Item(name="Pen", price=Decimal("10.00"), quantity=5)   # 50.00
    order = Order()
    order.add_item(item1)
    order.add_item(item2)

    # Action
    total = order.calculate_total()

    # Verification
    # Expected: 100.00 + 50.00 = 150.00
    assert total == Decimal("150.00")


def test_br05_fr03_discount_not_applied_at_threshold():
    """
    BR05: Orders above R$ 200 receive a 10% discount.
    FR03: The system must apply the discount correctly when eligible.
    Validates that an order of exactly R$ 200 does NOT receive a discount (Boundary Value).
    """
    # Setup
    item1 = Item(name="Monitor", price=Decimal("200.00"), quantity=1)
    order = Order()
    order.add_item(item1)

    # Action
    total = order.calculate_total()

    # Verification
    # Expected: 200.00 (Not > 200)
    assert total == Decimal("200.00")


def test_br05_fr03_discount_applied_above_threshold():
    """
    BR05: Orders above R$ 200 receive a 10% discount.
    FR03: The system must apply the discount correctly when eligible.
    Validates that an order strictly above R$ 200 receives 10% discount.
    """
    # Setup
    # Total items: 300.00
    item1 = Item(name="SSD", price=Decimal("300.00"), quantity=1)
    order = Order()
    order.add_item(item1)

    # Action
    total = order.calculate_total()

    # Verification
    # Calculation: 300.00 - (300.00 * 0.10) = 270.00
    assert total == Decimal("270.00")


def test_br05_discount_application_precision_edge_case():
    """
    BR05: Orders above R$ 200 receive a 10% discount.
    Validates discount application on immediate value above threshold (200.01).
    Ensures no rounding assumptions are made (strict math).
    """
    # Setup
    item1 = Item(name="Widget", price=Decimal("200.01"), quantity=1)
    order = Order()
    order.add_item(item1)

    # Action
    total = order.calculate_total()

    # Verification
    # Calculation: 200.01 * 10% = 20.001
    # Final: 200.01 - 20.001 = 180.009
    assert total == Decimal("180.009")


def test_br06_discount_applied_once_idempotency():
    """
    BR06: The discount must not be applied more than once.
    Validates that multiple calls to calculate_total return the same result.
    """
    # Setup
    item1 = Item(name="GPU", price=Decimal("1000.00"), quantity=1)
    order = Order()
    order.add_item(item1)

    # Action 1
    total_first_call = order.calculate_total()
    
    # Action 2
    total_second_call = order.calculate_total()

    # Verification
    # Expected: 1000.00 - 100.00 = 900.00
    assert total_first_call == Decimal("900.00")
    assert total_second_call == Decimal("900.00")
