import pytest
from decimal import Decimal
from cases.case02 import Item, Order

# BR01 – An order must contain at least one item
def test_br01_order_with_one_item_is_allowed():
    # BR01 – An order must contain at least one item
    order = Order()
    order.add_item(Item(name="Widget", price=Decimal("10.00"), quantity=1))
    result = order.calculate_total()
    # Validate: calculate_total returns a Decimal (no exception for valid order)
    assert isinstance(result, Decimal)

# BR01 – An order must contain at least one item
def test_br01_empty_order_raises_exception_when_calculating_total():
    # BR01 – An order must contain at least one item
    order = Order()
    # Validate: calculating total on an order with no items raises an exception
    with pytest.raises(Exception):
        order.calculate_total()

# BR02 – Each item must have a minimum quantity of 1
def test_br02_item_with_quantity_one_is_allowed():
    # BR02 – Each item must have a minimum quantity of 1
    order = Order()
    order.add_item(Item(name="Single", price=Decimal("5.00"), quantity=1))
    result = order.calculate_total()
    # Validate: calculate_total succeeds and returns a Decimal for item with quantity 1
    assert isinstance(result, Decimal)

# BR02 – Each item must have a minimum quantity of 1
def test_br02_item_with_quantity_zero_raises_exception():
    # BR02 – Each item must have a minimum quantity of 1
    order = Order()
    order.add_item(Item(name="ZeroQty", price=Decimal("5.00"), quantity=0))
    # Validate: quantity 0 is invalid and should cause an exception when calculating total
    with pytest.raises(Exception):
        order.calculate_total()

# BR03 – All items must have a positive price
def test_br03_item_with_positive_price_is_allowed():
    # BR03 – All items must have a positive price
    order = Order()
    order.add_item(Item(name="Cheap", price=Decimal("0.01"), quantity=1))
    result = order.calculate_total()
    # Validate: positive price allowed; calculate_total returns a Decimal
    assert isinstance(result, Decimal)

# BR03 – All items must have a positive price
def test_br03_item_with_zero_price_raises_exception():
    # BR03 – All items must have a positive price
    order = Order()
    order.add_item(Item(name="Free", price=Decimal("0.00"), quantity=1))
    # Validate: zero price is invalid and should cause an exception when calculating total
    with pytest.raises(Exception):
        order.calculate_total()

# BR04 – The total order value is the sum of the items
def test_br04_total_is_sum_of_items_exact_values():
    # BR04 – The total order value is the sum of the items
    order = Order()
    order.add_item(Item(name="A", price=Decimal("50.00"), quantity=1))
    order.add_item(Item(name="B", price=Decimal("100.00"), quantity=1))
    order.add_item(Item(name="C", price=Decimal("0.00"), quantity=0))  # intentionally invalid but not added effectfully
    # Use items that sum to a precise known total
    order = Order()
    order.add_item(Item(name="A", price=Decimal("60.00"), quantity=1))
    order.add_item(Item(name="B", price=Decimal("90.00"), quantity=1))
    expected = Decimal("150.00")
    result = order.calculate_total()
    # Validate: total equals the exact sum of item price * quantity
    assert result == expected

# FR02 – Correctly calculate the total
def test_fr02_calculate_total_with_multiple_items_exact_sum():
    # FR02 – Correctly calculate the total
    order = Order()
    order.add_item(Item(name="X", price=Decimal("50.00"), quantity=1))
    order.add_item(Item(name="Y", price=Decimal("73.45"), quantity=1))
    expected = Decimal("123.45")
    result = order.calculate_total()
    # Validate: calculate_total returns the exact expected total
    assert result == expected

# BR05 – Orders above R$ 200 receive a 10% discount
def test_br05_discount_applied_for_orders_strictly_above_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="Expensive", price=Decimal("250.00"), quantity=1))
    expected = Decimal("225.00")  # 250.00 * 0.9
    result = order.calculate_total()
    # Validate: discount applied once to orders strictly greater than 200
    assert result == expected

# BR05 – Orders above R$ 200 receive a 10% discount (edge case: exactly 200 should NOT get discount)
def test_br05_no_discount_for_order_equal_200():
    # BR05 – Orders above R$ 200 receive a 10% discount
    order = Order()
    order.add_item(Item(name="Boundary", price=Decimal("200.00"), quantity=1))
    expected = Decimal("200.00")
    result = order.calculate_total()
    # Validate: order equal to 200 does not receive the discount
    assert result == expected

# FR03 – The system must apply the discount correctly when eligible
def test_fr03_discount_calculation_for_201():
    # FR03 – The system must apply the discount correctly when eligible
    order = Order()
    order.add_item(Item(name="JustAbove", price=Decimal("201"), quantity=1))
    expected = Decimal("180.9")  # 201 * 0.9
    result = order.calculate_total()
    # Validate: discount correctly applied for a total of 201
    assert result == expected

# BR06 – The discount must not be applied more than once
def test_br06_discount_not_applied_more_than_once_on_multiple_calculations():
    # BR06 – The discount must not be applied more than once
    order = Order()
    order.add_item(Item(name="Big", price=Decimal("300.00"), quantity=1))
    first = order.calculate_total()
    second = order.calculate_total()
    # Validate: repeated calls do not further reduce the total; both calls equal expected discounted value
    assert first == second == Decimal("270.00")  # 300 * 0.9

# FR01 – Create an order with multiple items
def test_fr01_create_order_with_multiple_items_does_not_raise_and_returns_decimal():
    # FR01 – Create an order with multiple items
    order = Order()
    order.add_item(Item(name="One", price=Decimal("10.00"), quantity=2))
    order.add_item(Item(name="Two", price=Decimal("5.00"), quantity=3))
    result = order.calculate_total()
    # Validate: creating order with multiple items succeeds and calculate_total returns a Decimal
    assert isinstance(result, Decimal)

# FR04 – The system must display the final order value
def test_fr04_calculate_total_returns_final_order_value_for_non_discounted_order():
    # FR04 – The system must display the final order value
    order = Order()
    order.add_item(Item(name="Simple", price=Decimal("100.00"), quantity=1))
    expected = Decimal("100.00")
    result = order.calculate_total()
    # Validate: calculate_total returns the final order value (no discount applied)
    assert result == expected

# FR05 – The system must raise an exception in case of a failure
def test_fr05_system_raises_exception_for_negative_price_item():
    # FR05 – The system must raise an exception in case of a failure
    order = Order()
    order.add_item(Item(name="BadPrice", price=Decimal("-1.00"), quantity=1))
    # Validate: negative price constitutes a failure and causes an exception when calculating total
    with pytest.raises(Exception):
        order.calculate_total()