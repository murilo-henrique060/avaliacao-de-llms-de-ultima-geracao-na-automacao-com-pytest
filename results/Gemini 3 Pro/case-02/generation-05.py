
import pytest
from decimal import Decimal

from cases.case02 import Item, Order  # type: ignore

# Note: The following tests assume the existence of 'Item' and 'Order' classes 
# as described in the System Context and Class Diagram. 
# They are not implemented here as per the instruction "Do not implement the system".
# Ideally, these would be imported like: from src.system import Item, Order

# ------------------------------------------------------------------------------------------
# BUSINESS RULE VALIDATIONS
# ------------------------------------------------------------------------------------------

def test_br01_validation_order_must_contain_at_least_one_item():
    """
    BR01 – An order must contain at least one item.
    FR05 – The system must raise an exception in case of a failure.
    
    Validates that attempting to calculate the total of an empty order raises an exception.
    """
    order = Order()
    # The order is empty, so calculating total should be considered a failure/invalid state
    with pytest.raises(Exception):
        order.calculate_total()

def test_br02_validation_item_quantity_minimum_one_zero_value():
    """
    BR02 – Each item must have a minimum quantity of 1.
    FR05 – The system must raise an exception in case of a failure.
    
    Validates that creating an item with quantity 0 raises an exception.
    """
    with pytest.raises(Exception):
        Item(name="Invalid Item", price=Decimal("10.00"), quantity=0)

def test_br02_validation_item_quantity_minimum_one_negative_value():
    """
    BR02 – Each item must have a minimum quantity of 1.
    FR05 – The system must raise an exception in case of a failure.
    
    Validates that creating an item with negative quantity raises an exception.
    """
    with pytest.raises(Exception):
        Item(name="Invalid Item", price=Decimal("10.00"), quantity=-1)

def test_br03_validation_item_price_must_be_positive_zero():
    """
    BR03 – All items must have a positive price.
    FR05 – The system must raise an exception in case of a failure.
    
    Validates that creating an item with price 0.00 raises an exception.
    """
    with pytest.raises(Exception):
        Item(name="Free Item", price=Decimal("0.00"), quantity=1)

def test_br03_validation_item_price_must_be_positive_negative():
    """
    BR03 – All items must have a positive price.
    FR05 – The system must raise an exception in case of a failure.
    
    Validates that creating an item with a negative price raises an exception.
    """
    with pytest.raises(Exception):
        Item(name="Negative Price Item", price=Decimal("-10.00"), quantity=1)

def test_br04_calculation_total_order_value_sum_of_items_no_discount():
    """
    BR04 – The total order value is the sum of the items.
    FR02 – Correctly calculate the total.
    FR04 – The system must display the final order value.
    
    Scenario: Order with total value below discount threshold (R$ 150.00).
    Calculation: (50.00 * 2) + (50.00 * 1) = 150.00
    """
    order = Order()
    item1 = Item(name="Item A", price=Decimal("50.00"), quantity=2) # 100.00
    item2 = Item(name="Item B", price=Decimal("50.00"), quantity=1) # 50.00
    
    order.add_item(item1)
    order.add_item(item2)
    
    final_value = order.calculate_total()
    
    assert final_value == Decimal("150.00")

def test_br05_discount_rule_not_applied_exact_boundary():
    """
    BR05 – Orders above R$ 200 receive a 10% discount.
    
    Scenario: Total is exactly R$ 200.00.
    Rule logic: "Above" implies > 200. Exact 200 does not qualify.
    Expected: No discount applied.
    """
    order = Order()
    # 2 items of 100.00 = 200.00
    item = Item(name="Threshold Item", price=Decimal("100.00"), quantity=2)
    order.add_item(item)
    
    final_value = order.calculate_total()
    
    # Expect exact sum without discount
    assert final_value == Decimal("200.00")

def test_br05_discount_rule_applied_above_boundary():
    """
    BR05 – Orders above R$ 200 receive a 10% discount.
    FR03 – The system must apply the discount correctly when eligible.
    
    Scenario: Total is R$ 200.01 (smallest increment above 200 assuming 2 decimal places input).
    Calculation: 200.01 * 0.90 (10% off) = 180.009
    """
    order = Order()
    # 1 item of 200.01
    item = Item(name="Eligible Item", price=Decimal("200.01"), quantity=1)
    order.add_item(item)
    
    final_value = order.calculate_total()
    
    # 200.01 - 10% (20.001) = 180.009
    # Using strict Decimal comparison without rounding assumptions as per constraint #2
    expected_value = Decimal("200.01") * Decimal("0.9") 
    
    assert final_value == expected_value

def test_br05_discount_calculation_high_value():
    """
    BR05 – Orders above R$ 200 receive a 10% discount.
    FR02 – Correctly calculate the total.
    
    Scenario: Total is R$ 1000.00.
    Calculation: 1000.00 * 0.90 = 900.00
    """
    order = Order()
    item = Item(name="Expensive Item", price=Decimal("1000.00"), quantity=1)
    order.add_item(item)
    
    final_value = order.calculate_total()
    
    assert final_value == Decimal("900.00")

def test_br06_discount_application_idempotency():
    """
    BR06 – The discount must not be applied more than once.
    FR03 – The system must apply the discount correctly when eligible.
    
    Scenario: Call calculate_total multiple times on an eligible order.
    The result must remain consistent and not apply the discount recursively.
    """
    order = Order()
    item = Item(name="Item for Idempotency", price=Decimal("300.00"), quantity=1)
    order.add_item(item)
    
    # First calculation: 300 * 0.9 = 270.00
    first_calc = order.calculate_total()
    assert first_calc == Decimal("270.00")
    
    # Second calculation: Should still be 270.00, not 270 * 0.9
    second_calc = order.calculate_total()
    assert second_calc == Decimal("270.00")

# ------------------------------------------------------------------------------------------
# FUNCTIONAL REQUIREMENT VALIDATIONS
# ------------------------------------------------------------------------------------------

def test_fr01_create_order_with_multiple_items_and_quantities():
    """
    FR01 – Create an order with multiple items.
    FR02 – Correctly calculate the total.
    BR02 – Each item must have a minimum quantity of 1 (Implicitly validated by success).
    
    Validates the ability to add distinct items with different quantities to a single order.
    """
    order = Order()
    item1 = Item(name="Pencil", price=Decimal("1.50"), quantity=10) # 15.00
    item2 = Item(name="Notebook", price=Decimal("20.00"), quantity=2) # 40.00
    item3 = Item(name="Eraser", price=Decimal("5.00"), quantity=1) # 5.00
    
    order.add_item(item1)
    order.add_item(item2)
    order.add_item(item3)
    
    # Total: 15 + 40 + 5 = 60.00 (Below 200, no discount)
    final_value = order.calculate_total()
    
    assert final_value == Decimal("60.00")
