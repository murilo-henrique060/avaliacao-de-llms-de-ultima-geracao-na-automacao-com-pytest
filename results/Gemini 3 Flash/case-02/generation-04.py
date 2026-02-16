
import pytest
from decimal import Decimal

from cases.case02 import Item, Order  # type: ignore

# Assuming the existence of Item and Order classes as per UML
# from system import Item, Order

# BR01 – An order must contain at least one item
# FR05 – The system must raise an exception in case of a failure
def test_order_calculation_fails_without_items():
    order = Order()
    with pytest.raises(Exception):
        order.calculate_total()

# BR01 – An order must contain at least one item
# FR01 – Create an order with multiple items
def test_order_with_multiple_items_is_valid():
    order = Order()
    item1 = Item(name="Product A", price=Decimal("10.00"), quantity=1)
    item2 = Item(name="Product B", price=Decimal("20.00"), quantity=2)
    order.add_item(item1)
    order.add_item(item2)
    # Validation occurs by successfully calculating total without exception
    assert order.calculate_total() == Decimal("50.00")

# BR02 – Each item must have a minimum quantity of 1
# FR05 – The system must raise an exception in case of a failure
def test_item_with_zero_quantity_raises_exception():
    with pytest.raises(Exception):
        Item(name="Invalid Item", price=Decimal("10.00"), quantity=0)

# BR02 – Each item must have a minimum quantity of 1
# FR05 – The system must raise an exception in case of a failure
def test_item_with_negative_quantity_raises_exception():
    with pytest.raises(Exception):
        Item(name="Invalid Item", price=Decimal("10.00"), quantity=-1)

# BR03 – All items must have a positive price
# FR05 – The system must raise an exception in case of a failure
def test_item_with_zero_price_raises_exception():
    with pytest.raises(Exception):
        Item(name="Free Item", price=Decimal("0.00"), quantity=1)

# BR03 – All items must have a positive price
# FR05 – The system must raise an exception in case of a failure
def test_item_with_negative_price_raises_exception():
    with pytest.raises(Exception):
        Item(name="Debt Item", price=Decimal("-5.00"), quantity=1)

# BR04 – The total order value is the sum of the items
# FR02 – Correctly calculate the total
def test_total_calculation_is_exact_sum_of_items():
    order = Order()
    order.add_item(Item(name="Item 1", price=Decimal("50.00"), quantity=2)) # 100
    order.add_item(Item(name="Item 2", price=Decimal("25.50"), quantity=1)) # 25.50
    # Total 125.50 (No discount as it is <= 200)
    assert order.calculate_total() == Decimal("125.50")

# BR05 – Orders above R$ 200 receive a 10% discount
# FR03 – The system must apply the discount correctly when eligible
def test_order_above_200_receives_ten_percent_discount():
    order = Order()
    # Total: 250.00
    order.add_item(Item(name="Expensive Item", price=Decimal("250.00"), quantity=1))
    # Discount: 25.00 (10% of 250)
    # Expected: 225.00
    assert order.calculate_total() == Decimal("225.00")

# BR05 – Orders above R$ 200 receive a 10% discount
def test_order_of_exactly_200_receives_no_discount():
    order = Order()
    # Total: 200.00
    order.add_item(Item(name="Border Item", price=Decimal("100.00"), quantity=2))
    # Requirement says "above 200", so 200 should not have discount
    assert order.calculate_total() == Decimal("200.00")

# BR05 – Orders above R$ 200 receive a 10% discount
# FR04 – The system must display the final order value
def test_order_slightly_above_200_applies_discount_precisely():
    order = Order()
    # Total: 200.01
    order.add_item(Item(name="Edge Item", price=Decimal("200.01"), quantity=1))
    # 10% of 200.01 = 20.001
    # Result: 200.01 - 20.001 = 180.009
    assert order.calculate_total() == Decimal("180.009")

# BR06 – The discount must not be applied more than once
def test_discount_is_not_cumulative_on_multiple_calls():
    order = Order()
    order.add_item(Item(name="High Value", price=Decimal("300.00"), quantity=1))
    
    first_calculation = order.calculate_total() # 270.00
    second_calculation = order.calculate_total() # Must still be 270.00
    
    assert first_calculation == Decimal("270.00")
    assert second_calculation == Decimal("270.00")
