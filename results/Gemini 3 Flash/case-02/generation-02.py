
import pytest
from decimal import Decimal

from cases.case02 import Item, Order  # type: ignore

# BR01 – An order must contain at least one item
# FR01 – Create an order with multiple items
def test_br01_fr01_create_order_with_items():
    order = Order()
    item1 = Item(name="Product A", price=Decimal("50.00"), quantity=1)
    item2 = Item(name="Product B", price=Decimal("30.00"), quantity=2)
    order.add_item(item1)
    order.add_item(item2)
    # Validates that an order can be created and items added without exception
    assert order.calculate_total() == Decimal("110.00")

# BR01 – An order must contain at least one item
# FR05 – The system must raise an exception in case of a failure
def test_br01_fr05_empty_order_raises_exception():
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()

# BR02 – Each item must have a minimum quantity of 1
def test_br02_item_quantity_minimum_valid():
    order = Order()
    item = Item(name="Product A", price=Decimal("100.00"), quantity=1)
    order.add_item(item)
    assert order.calculate_total() == Decimal("100.00")

# BR02 – Each item must have a minimum quantity of 1
# FR05 – The system must raise an exception in case of a failure
def test_br02_fr05_item_quantity_zero_raises_exception():
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("100.00"), quantity=0)

# BR02 – Each item must have a minimum quantity of 1
# FR05 – The system must raise an exception in case of a failure
def test_br02_fr05_item_quantity_negative_raises_exception():
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("100.00"), quantity=-5)

# BR03 – All items must have a positive price
def test_br03_item_price_positive_valid():
    order = Order()
    item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
    order.add_item(item)
    assert order.calculate_total() == Decimal("0.01")

# BR03 – All items must have a positive price
# FR05 – The system must raise an exception in case of a failure
def test_br03_fr05_item_price_zero_raises_exception():
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("0.00"), quantity=1)

# BR03 – All items must have a positive price
# FR05 – The system must raise an exception in case of a failure
def test_br03_fr05_item_price_negative_raises_exception():
    with pytest.raises(Exception):
        Item(name="Product A", price=Decimal("-10.00"), quantity=1)

# BR04 – The total order value is the sum of the items
# FR02 – Correctly calculate the total
def test_br04_fr02_calculate_total_sum_of_items():
    order = Order()
    order.add_item(Item(name="Item 1", price=Decimal("10.00"), quantity=2)) # 20.00
    order.add_item(Item(name="Item 2", price=Decimal("15.50"), quantity=1)) # 15.50
    # FR04 – The system must display the final order value
    assert order.calculate_total() == Decimal("35.50")

# BR05 – Orders above R$ 200 receive a 10% discount
def test_br05_no_discount_at_threshold_value():
    order = Order()
    order.add_item(Item(name="Expensive Item", price=Decimal("200.00"), quantity=1))
    # FR04 – The system must display the final order value
    assert order.calculate_total() == Decimal("200.00")

# BR05 – Orders above R$ 200 receive a 10% discount
# FR03 – The system must apply the discount correctly when eligible
def test_br05_fr03_discount_applied_above_threshold():
    order = Order()
    # 200.01 is above 200.00
    order.add_item(Item(name="Item", price=Decimal("200.01"), quantity=1))
    # 200.01 - 10% (20.001) = 180.009
    assert order.calculate_total() == Decimal("180.009")

# BR05 – Orders above R$ 200 receive a 10% discount
# FR03 – The system must apply the discount correctly when eligible
def test_br05_fr03_discount_applied_on_large_total():
    order = Order()
    order.add_item(Item(name="Item 1", price=Decimal("150.00"), quantity=1))
    order.add_item(Item(name="Item 2", price=Decimal("150.00"), quantity=1))
    # Total 300.00 -> Discount 30.00 -> Final 270.00
    assert order.calculate_total() == Decimal("270.00")

# BR06 – The discount must not be applied more than once
def test_br06_discount_idempotency():
    order = Order()
    order.add_item(Item(name="Item", price=Decimal("300.00"), quantity=1))
    first_calculation = order.calculate_total()
    second_calculation = order.calculate_total()
    assert first_calculation == Decimal("270.00")
    assert second_calculation == Decimal("270.00")
    assert first_calculation == second_calculation
