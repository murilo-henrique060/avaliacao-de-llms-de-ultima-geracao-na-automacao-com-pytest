
import pytest
from decimal import Decimal

from cases.case02 import Item, Order  # type: ignore
# Note: The following tests assume the existence of classes Item and Order 
# as defined in the provided UML class diagram.

# BR01 – An order must contain at least one item
# FR01 – Create an order with multiple items
def test_br01_positive_order_with_one_item_is_allowed():
    order = Order()
    item = Item(name="Product A", price=Decimal("100.00"), quantity=1)
    order.add_item(item)
    assert order.calculate_total() == Decimal("100.00")

# BR01 – An order must contain at least one item
# FR05 – The system must raise an exception in case of a failure
def test_br01_negative_order_with_no_items_raises_exception():
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()

# BR02 – Each item must have a minimum quantity of 1
def test_br02_positive_item_with_quantity_one_is_allowed():
    item = Item(name="Product A", price=Decimal("10.00"), quantity=1)
    assert item.quantity == 1

# BR02 – Each item must have a minimum quantity of 1
# FR05 – The system must raise an exception in case of a failure
def test_br02_negative_item_with_quantity_zero_raises_exception():
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("10.00"), quantity=0)

# BR03 – All items must have a positive price
def test_br03_positive_item_with_minimum_positive_price():
    item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
    assert item.price == Decimal("0.01")

# BR03 – All items must have a positive price
# FR05 – The system must raise an exception in case of a failure
def test_br03_negative_item_with_zero_price_raises_exception():
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("0.00"), quantity=1)

# BR03 – All items must have a positive price
# FR05 – The system must raise an exception in case of a failure
def test_br03_negative_item_with_negative_price_raises_exception():
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("-5.00"), quantity=1)

# BR04 – The total order value is the sum of the items
# FR02 – Correctly calculate the total
def test_br04_total_calculation_sum_of_multiple_items():
    order = Order()
    order.add_item(Item(name="Item 1", price=Decimal("50.00"), quantity=2))
    order.add_item(Item(name="Item 2", price=Decimal("30.00"), quantity=1))
    # Calculation: (50.00 * 2) + (30.00 * 1) = 130.00
    assert order.calculate_total() == Decimal("130.00")

# BR05 – Orders above R$ 200 receive a 10% discount
def test_br05_order_with_exactly_200_does_not_receive_discount():
    order = Order()
    order.add_item(Item(name="Expensive Item", price=Decimal("200.00"), quantity=1))
    assert order.calculate_total() == Decimal("200.00")

# BR05 – Orders above R$ 200 receive a 10% discount
# FR03 – The system must apply the discount correctly when eligible
def test_br05_order_above_200_receives_ten_percent_discount():
    order = Order()
    order.add_item(Item(name="Expensive Item", price=Decimal("200.01"), quantity=1))
    # Calculation: 200.01 * 0.90 = 180.009
    assert order.calculate_total() == Decimal("180.009")

# BR06 – The discount must not be applied more than once
def test_br06_discount_is_not_applied_cumulatively_on_repeated_calls():
    order = Order()
    order.add_item(Item(name="Item", price=Decimal("300.00"), quantity=1))
    first_calculation = order.calculate_total()
    second_calculation = order.calculate_total()
    # 300.00 - 10% = 270.00. Should remain 270.00.
    assert first_calculation == Decimal("270.00")
    assert second_calculation == Decimal("270.00")

# FR01 – Create an order with multiple items
def test_fr01_add_multiple_items_to_single_order():
    order = Order()
    item1 = Item(name="A", price=Decimal("10.00"), quantity=1)
    item2 = Item(name="B", price=Decimal("20.00"), quantity=1)
    item3 = Item(name="C", price=Decimal("30.00"), quantity=1)
    order.add_item(item1)
    order.add_item(item2)
    order.add_item(item3)
    assert order.calculate_total() == Decimal("60.00")

# FR04 – The system must display the final order value
def test_fr04_calculate_total_returns_precise_decimal_value():
    order = Order()
    order.add_item(Item(name="Product", price=Decimal("15.55"), quantity=1))
    result = order.calculate_total()
    assert result == Decimal("15.55")
    assert isinstance(result, Decimal)
