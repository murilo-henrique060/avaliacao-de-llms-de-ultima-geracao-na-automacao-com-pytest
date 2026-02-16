
import pytest
from decimal import Decimal

from cases.case02 import Item, Order  # type: ignore

# Note: Implementation of Item and Order classes is assumed to exist as per the Class Diagram.

def test_br01_order_with_one_item_is_valid():
    # BR01 – An order must contain at least one item
    order = Order()
    item = Item(name="Product A", price=Decimal("10.00"), quantity=1)
    order.add_item(item)
    assert order.calculate_total() == Decimal("10.00")

def test_br01_order_with_no_items_raises_exception():
    # BR01 – An order must contain at least one item
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()

def test_br02_item_quantity_minimum_is_one():
    # BR02 – Each item must have a minimum quantity of 1
    item = Item(name="Product A", price=Decimal("10.00"), quantity=1)
    assert item.quantity == 1

def test_br02_item_quantity_less_than_one_raises_exception():
    # BR02 – Each item must have a minimum quantity of 1
    # FR05 – The system must raise an exception in case of a failure
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("10.00"), quantity=0)

def test_br03_item_price_must_be_positive():
    # BR03 – All items must have a positive price
    item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
    assert item.price > 0

def test_br03_item_price_zero_raises_exception():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("0.00"), quantity=1)

def test_br03_item_price_negative_raises_exception():
    # BR03 – All items must have a positive price
    # FR05 – The system must raise an exception in case of a failure
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("-10.00"), quantity=1)

def test_br04_fr02_total_calculation_is_sum_of_items():
    # BR04 – The total order value is the sum of the items
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="Item 1", price=Decimal("50.00"), quantity=1))
    order.add_item(Item(name="Item 2", price=Decimal("25.00"), quantity=2))
    # Sum: 50.00 + (25.00 * 2) = 100.00
    assert order.calculate_total() == Decimal("100.00")

def test_br05_fr03_discount_applied_above_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    # FR03 – The system must apply the discount correctly when eligible
    order = Order()
    order.add_item(Item(name="Expensive Item", price=Decimal("210.00"), quantity=1))
    # 210.00 * 0.90 = 189.00
    assert order.calculate_total() == Decimal("189.00")

def test_br05_no_discount_at_exactly_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="Edge Item", price=Decimal("200.00"), quantity=1))
    assert order.calculate_total() == Decimal("200.00")

def test_br05_no_discount_below_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="Cheap Item", price=Decimal("199.99"), quantity=1))
    assert order.calculate_total() == Decimal("199.99")

def test_br06_discount_not_applied_more_than_once():
    # BR06 – The discount must not be applied more than once
    order = Order()
    order.add_item(Item(name="Expensive Item", price=Decimal("300.00"), quantity=1))
    # First calculation: 300 - 10% = 270
    first_calc = order.calculate_total()
    # Second calculation must remain 270, not apply 10% over 270 again
    second_calc = order.calculate_total()
    assert first_calc == Decimal("270.00")
    assert second_calc == Decimal("270.00")

def test_fr01_create_order_with_multiple_items():
    # FR01 – Create an order with multiple items
    order = Order()
    item1 = Item(name="Item 1", price=Decimal("10.00"), quantity=1)
    item2 = Item(name="Item 2", price=Decimal("20.00"), quantity=1)
    item3 = Item(name="Item 3", price=Decimal("30.00"), quantity=1)
    order.add_item(item1)
    order.add_item(item2)
    order.add_item(item3)
    assert order.calculate_total() == Decimal("60.00")

def test_fr04_display_final_order_value():
    # FR04 – The system must display the final order value
    order = Order()
    order.add_item(Item(name="Product", price=Decimal("100.00"), quantity=1))
    final_value = order.calculate_total()
    assert isinstance(final_value, Decimal)
    assert final_value == Decimal("100.00")
