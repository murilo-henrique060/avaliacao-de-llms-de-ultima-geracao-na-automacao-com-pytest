
import pytest
from decimal import Decimal

from cases.case02 import Item, Order  # type: ignore

# The tests below assume the existence of classes Item and Order as specified in the UML.
# Each test validates a specific Business Rule (BR) or Functional Requirement (FR).

def test_br01_order_calculation_fails_without_items():
    # BR01 – An order must contain at least one item
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()

def test_br01_order_with_single_item_is_valid():
    # BR01 – An order must contain at least one item
    order = Order()
    item = Item(name="Valid Item", price=Decimal("10.00"), quantity=1)
    order.add_item(item)
    assert order.calculate_total() == Decimal("10.00")

def test_br02_item_with_zero_quantity_is_invalid():
    # BR02 – Each item must have a minimum quantity of 1
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        item = Item(name="Invalid Quantity", price=Decimal("10.00"), quantity=0)
        order.add_item(item)

def test_br02_item_with_minimum_quantity_one_is_valid():
    # BR02 – Each item must have a minimum quantity of 1
    order = Order()
    item = Item(name="Min Quantity", price=Decimal("10.00"), quantity=1)
    order.add_item(item)
    assert order.calculate_total() == Decimal("10.00")

def test_br03_item_with_zero_price_is_invalid():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        item = Item(name="Zero Price", price=Decimal("0.00"), quantity=1)
        order.add_item(item)

def test_br03_item_with_negative_price_is_invalid():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        item = Item(name="Negative Price", price=Decimal("-1.50"), quantity=1)
        order.add_item(item)

def test_br04_total_is_the_sum_of_item_prices_and_quantities():
    # BR04 – The total order value is the sum of the items
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="Item A", price=Decimal("10.00"), quantity=2))
    order.add_item(Item(name="Item B", price=Decimal("5.00"), quantity=1))
    # Calculation: (10.00 * 2) + (5.00 * 1) = 25.00
    assert order.calculate_total() == Decimal("25.00")

def test_br05_discount_applied_when_total_strictly_above_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    # FR03 – The system must apply the discount correctly when eligible
    order = Order()
    order.add_item(Item(name="Expensive Item", price=Decimal("210.00"), quantity=1))
    # Calculation: 210.00 - 10% = 189.00
    assert order.calculate_total() == Decimal("189.00")

def test_br05_no_discount_when_total_is_exactly_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="Boundary Item", price=Decimal("200.00"), quantity=1))
    # 200.00 is not "above" 200.00, so no discount should be applied.
    assert order.calculate_total() == Decimal("200.00")

def test_br05_discount_applied_on_minimum_value_above_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="Over Boundary", price=Decimal("200.01"), quantity=1))
    # Calculation: 200.01 - (200.01 * 0.10) = 180.009
    assert order.calculate_total() == Decimal("180.009")

def test_br06_discount_not_applied_consecutively():
    # BR06 – The discount must not be applied more than once
    order = Order()
    order.add_item(Item(name="Item", price=Decimal("300.00"), quantity=1))
    # First calculation: 300.00 - 10% = 270.00
    first_result = order.calculate_total()
    # Second calculation should return the same value without applying another discount on 270.00
    second_result = order.calculate_total()
    assert first_result == Decimal("270.00")
    assert second_result == Decimal("270.00")

def test_fr01_create_order_with_multiple_items_validation():
    # FR01 – Create an order with multiple items
    order = Order()
    order.add_item(Item(name="Item 1", price=Decimal("5.00"), quantity=1))
    order.add_item(Item(name="Item 2", price=Decimal("15.00"), quantity=2))
    order.add_item(Item(name="Item 3", price=Decimal("10.00"), quantity=1))
    # Functional check: (5*1) + (15*2) + (10*1) = 45.00
    assert order.calculate_total() == Decimal("45.00")

def test_fr04_calculate_total_returns_final_value():
    # FR04 – The system must display the final order value
    order = Order()
    order.add_item(Item(name="Display Product", price=Decimal("100.00"), quantity=1))
    result = order.calculate_total()
    # Check if a value is returned and matches the expected final total
    assert result == Decimal("100.00")
