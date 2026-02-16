
import pytest
from decimal import Decimal

from cases.case02 import Item, Order  # type: ignore

# Note: The tests below assume that 'Order' and 'Item' classes are available 
# and imported from the application module (e.g., from app import Order, Item).
# Since the implementation is not provided, these tests focus purely on the interface 
# and expected behaviors defined in the specifications.

# -----------------------------------------------------------------------------
# Business Rule: BR02 - Each item must have a minimum quantity of 1
# Functional Requirement: FR05 - The system must raise an exception in case of a failure
# -----------------------------------------------------------------------------

def test_item_creation_raises_exception_for_zero_quantity():
    # BR02 – Each item must have a minimum quantity of 1
    # FR05 – The system must raise an exception in case of a failure
    item_name = "Widget A"
    item_price = Decimal("10.00")
    invalid_quantity = 0

    with pytest.raises(Exception):
        Item(name=item_name, price=item_price, quantity=invalid_quantity)

def test_item_creation_raises_exception_for_negative_quantity():
    # BR02 – Each item must have a minimum quantity of 1
    # FR05 – The system must raise an exception in case of a failure
    item_name = "Widget B"
    item_price = Decimal("10.00")
    invalid_quantity = -5

    with pytest.raises(Exception):
        Item(name=item_name, price=item_price, quantity=invalid_quantity)

# -----------------------------------------------------------------------------
# Business Rule: BR03 - All items must have a positive price
# Functional Requirement: FR05 - The system must raise an exception in case of a failure
# -----------------------------------------------------------------------------

def test_item_creation_raises_exception_for_zero_price():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    item_name = "Free Gift"
    invalid_price = Decimal("0.00")
    quantity = 1

    with pytest.raises(Exception):
        Item(name=item_name, price=invalid_price, quantity=quantity)

def test_item_creation_raises_exception_for_negative_price():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    item_name = "Debt"
    invalid_price = Decimal("-10.00")
    quantity = 1

    with pytest.raises(Exception):
        Item(name=item_name, price=invalid_price, quantity=quantity)

# -----------------------------------------------------------------------------
# Business Rule: BR01 - An order must contain at least one item
# Functional Requirement: FR05 - The system must raise an exception in case of a failure
# -----------------------------------------------------------------------------

def test_order_calculation_raises_exception_when_empty():
    # BR01 – An order must contain at least one item
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    
    # We expect the validation to occur when trying to process/calculate the order
    with pytest.raises(Exception):
        order.calculate_total()

# -----------------------------------------------------------------------------
# Business Rule: BR04 - The total order value is the sum of the items
# Functional Requirements: FR01, FR02, FR04
# -----------------------------------------------------------------------------

def test_calculate_total_sum_of_items_below_discount_threshold():
    # BR04 – The total order value is the sum of the items
    # FR01 – Create an order with multiple items
    # FR02 – Correctly calculate the total
    # FR04 – The system must display the final order value
    
    order = Order()
    # Item 1: 50.00 * 2 = 100.00
    item1 = Item(name="Product A", price=Decimal("50.00"), quantity=2)
    # Item 2: 30.00 * 1 = 30.00
    item2 = Item(name="Product B", price=Decimal("30.00"), quantity=1)
    
    order.add_item(item1)
    order.add_item(item2)
    
    # Total expected: 130.00 (Below 200.00, so no discount)
    expected_total = Decimal("130.00")
    
    assert order.calculate_total() == expected_total

# -----------------------------------------------------------------------------
# Business Rule: BR05 - Orders above R$ 200 receive a 10% discount
# Functional Requirements: FR03 - The system must apply the discount correctly when eligible
# -----------------------------------------------------------------------------

def test_calculate_total_exact_boundary_no_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    # FR03 – The system must apply the discount correctly when eligible
    # Scenario: Total is exactly 200.00 (Should NOT receive discount)
    
    order = Order()
    # 100.00 * 2 = 200.00
    item = Item(name="Threshold Product", price=Decimal("100.00"), quantity=2)
    
    order.add_item(item)
    
    expected_total = Decimal("200.00")
    
    assert order.calculate_total() == expected_total

def test_calculate_total_above_boundary_with_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    # FR03 – The system must apply the discount correctly when eligible
    # Scenario: Total is 201.00 (Above 200, receives 10% discount)
    
    order = Order()
    # 201.00 * 1 = 201.00
    item = Item(name="Premium Product", price=Decimal("201.00"), quantity=1)
    
    order.add_item(item)
    
    # Calculation: 201.00 - 10% = 201.00 - 20.10 = 180.90
    expected_total = Decimal("180.90")
    
    assert order.calculate_total() == expected_total

def test_calculate_total_above_boundary_small_increment_with_discount():
    # BR05 – Orders above R$ 200 receive a 10% discount
    # FR03 – The system must apply the discount correctly when eligible
    # Scenario: Total is 200.01 (Barely above 200, receives 10% discount)
    
    order = Order()
    item = Item(name="Edge Case Product", price=Decimal("200.01"), quantity=1)
    
    order.add_item(item)
    
    # Calculation: 200.01 * 0.9 = 180.009
    # No rounding specified in rules, requiring exact value
    expected_total = Decimal("180.009")
    
    assert order.calculate_total() == expected_total

# -----------------------------------------------------------------------------
# Business Rule: BR06 - The discount must not be applied more than once
# Functional Requirements: FR02, FR03
# -----------------------------------------------------------------------------

def test_discount_application_is_idempotent():
    # BR06 – The discount must not be applied more than once
    # FR02 – Correctly calculate the total
    
    order = Order()
    # 300.00 * 1 = 300.00 (Eligible for discount)
    item = Item(name="Expensive Item", price=Decimal("300.00"), quantity=1)
    order.add_item(item)
    
    # Expected: 300.00 * 0.9 = 270.00
    expected_total = Decimal("270.00")
    
    # First call
    first_calculation = order.calculate_total()
    assert first_calculation == expected_total
    
    # Second call - must not re-apply discount to the already discounted value
    # e.g., should not become 243.00
    second_calculation = order.calculate_total()
    assert second_calculation == expected_total
