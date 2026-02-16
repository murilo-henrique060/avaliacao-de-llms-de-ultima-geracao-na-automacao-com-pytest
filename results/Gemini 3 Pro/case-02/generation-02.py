
import pytest
from decimal import Decimal

# Assuming the existence of the classes based on the provided Class Diagram.
# In a real environment, these would be imported from the source module.
# from src.ecommerce import Order, Item, BusinessRuleException

# For the purpose of these tests, we assume a generic BusinessRuleException 
# is raised for domain violations, as requested in FR05/Evaluation Criteria.
# If the specific exception class is not defined, we catch Exception or a specific defined one.
# Here we refer to it as `BusinessRuleException` for clarity in the tests.

from cases.case02 import Item, Order  # type: ignore

class BusinessRuleException(Exception):
    pass

# -----------------------------------------------------------------------------------
# BUSINESS RULES (BR) & FUNCTIONAL REQUIREMENTS (FR) TESTS
# -----------------------------------------------------------------------------------

# BR02 – Each item must have a minimum quantity of 1
# FR05 – The system must raise an exception in case of a failure
def test_item_creation_with_valid_quantity():
    """
    Validates that an Item can be created with a positive integer quantity (>= 1).
    Fulfills BR02 (valid case).
    """
    item = Item(name="Notebook", price=Decimal("100.00"), quantity=1)
    assert item.quantity == 1

# BR02 – Each item must have a minimum quantity of 1
# FR05 – The system must raise an exception in case of a failure
def test_item_creation_with_zero_quantity_raises_exception():
    """
    Validates that creating an Item with quantity 0 raises an exception.
    Fulfills BR02 (violation case) and FR05.
    """
    with pytest.raises(BusinessRuleException):
        Item(name="Notebook", price=Decimal("100.00"), quantity=0)

# BR02 – Each item must have a minimum quantity of 1
# FR05 – The system must raise an exception in case of a failure
def test_item_creation_with_negative_quantity_raises_exception():
    """
    Validates that creating an Item with negative quantity raises an exception.
    Fulfills BR02 (violation case) and FR05.
    """
    with pytest.raises(BusinessRuleException):
        Item(name="Notebook", price=Decimal("100.00"), quantity=-1)

# BR03 – All items must have a positive price
# FR05 – The system must raise an exception in case of a failure
def test_item_creation_with_positive_price():
    """
    Validates that an Item can be created with a strictly positive price.
    Fulfills BR03 (valid case).
    """
    item = Item(name="Pencil", price=Decimal("0.01"), quantity=10)
    assert item.price == Decimal("0.01")

# BR03 – All items must have a positive price
# FR05 – The system must raise an exception in case of a failure
def test_item_creation_with_zero_price_raises_exception():
    """
    Validates that creating an Item with price 0.00 raises an exception.
    'Positive' strictly implies > 0.
    Fulfills BR03 (violation case) and FR05.
    """
    with pytest.raises(BusinessRuleException):
        Item(name="Free Sample", price=Decimal("0.00"), quantity=1)

# BR03 – All items must have a positive price
# FR05 – The system must raise an exception in case of a failure
def test_item_creation_with_negative_price_raises_exception():
    """
    Validates that creating an Item with negative price raises an exception.
    Fulfills BR03 (violation case) and FR05.
    """
    with pytest.raises(BusinessRuleException):
        Item(name="Debt", price=Decimal("-10.00"), quantity=1)

# FR01 – Create an order with multiple items
def test_create_order_with_multiple_items_successfully():
    """
    Validates that multiple items can be added to an order.
    Fulfills FR01.
    """
    order = Order()
    item1 = Item(name="Mouse", price=Decimal("50.00"), quantity=1)
    item2 = Item(name="Keyboard", price=Decimal("100.00"), quantity=1)
    
    order.add_item(item1)
    order.add_item(item2)
    
    # Validation occurs at total calculation or explicit checking, 
    # but here we ensure no error is raised during addition.

# BR01 – An order must contain at least one item
# FR05 – The system must raise an exception in case of a failure
def test_calculate_total_with_empty_order_raises_exception():
    """
    Validates that calculating the total of an empty order raises an exception.
    Fulfills BR01 and FR05.
    """
    order = Order()
    with pytest.raises(BusinessRuleException):
        order.calculate_total()

# BR04 – The total order value is the sum of the items
# FR02 – Correctly calculate the total
# FR04 – The system must display the final order value
def test_calculate_total_sum_of_items_no_discount():
    """
    Validates total calculation as simple sum when threshold is not met.
    Scenario: 2 items, total R$ 100.00 (below 200 threshold).
    Fulfills BR04, FR02, FR04.
    """
    order = Order()
    # 2 units of 25.00 = 50.00
    order.add_item(Item(name="Item A", price=Decimal("25.00"), quantity=2))
    # 1 unit of 50.00 = 50.00
    order.add_item(Item(name="Item B", price=Decimal("50.00"), quantity=1))
    
    # Total = 100.00
    result = order.calculate_total()
    assert result == Decimal("100.00")

# BR05 – Orders above R$ 200 receive a 10% discount
# FR03 – The system must apply the discount correctly when eligible
def test_calculate_total_exact_threshold_200_no_discount():
    """
    Validates boundary condition: Exactly R$ 200.00.
    Rule says 'above 200', so 200.00 should NOT receive discount.
    Fulfills BR05 (boundary check).
    """
    order = Order()
    order.add_item(Item(name="Threshold Item", price=Decimal("200.00"), quantity=1))
    
    result = order.calculate_total()
    assert result == Decimal("200.00")

# BR05 – Orders above R$ 200 receive a 10% discount
# FR03 – The system must apply the discount correctly when eligible
def test_calculate_total_just_above_threshold_applies_discount():
    """
    Validates boundary condition: R$ 200.01 (smallest realistic increment above 200).
    Should receive 10% discount.
    Calculation: 200.01 - (200.01 * 0.10) = 200.01 * 0.9 = 180.009
    Fulfills BR05.
    """
    order = Order()
    order.add_item(Item(name="Just Above", price=Decimal("200.01"), quantity=1))
    
    result = order.calculate_total()
    # Exact calculation expected: 180.009
    assert result == Decimal("180.009")

# BR05 – Orders above R$ 200 receive a 10% discount
# FR03 – The system must apply the discount correctly when eligible
def test_calculate_total_high_value_applies_discount():
    """
    Validates discount application for a standard high value case.
    Total Raw: 500.00
    Discount: 10% of 500 = 50
    Final: 450.00
    Fulfills BR05 and FR03.
    """
    order = Order()
    order.add_item(Item(name="Expensive Item", price=Decimal("500.00"), quantity=1))
    
    result = order.calculate_total()
    assert result == Decimal("450.00")

# BR06 – The discount must not be applied more than once
def test_calculate_total_idempotency_discount_applied_once():
    """
    Validates that calling calculate_total multiple times does not compound the discount.
    Raw: 300.00
    Expected: 270.00 (300 * 0.9)
    If applied twice, it would be 243.00.
    Fulfills BR06.
    """
    order = Order()
    order.add_item(Item(name="Item", price=Decimal("300.00"), quantity=1))
    
    first_call = order.calculate_total()
    assert first_call == Decimal("270.00")
    
    second_call = order.calculate_total()
    assert second_call == Decimal("270.00")

# BR04 – The total order value is the sum of the items
# BR05 – Orders above R$ 200 receive a 10% discount
def test_calculate_total_sum_accumulation_with_discount():
    """
    Validates that the sum accounts for quantity correctly before applying discount.
    Item 1: 5 * 20.00 = 100.00
    Item 2: 2 * 60.00 = 120.00
    Total Raw: 220.00
    Discount applicable (> 200).
    Expected: 220.00 * 0.9 = 198.00
    Fulfills BR04 (sum logic) and BR05 (discount logic).
    """
    order = Order()
    order.add_item(Item(name="Item A", price=Decimal("20.00"), quantity=5))
    order.add_item(Item(name="Item B", price=Decimal("60.00"), quantity=2))
    
    result = order.calculate_total()
    assert result == Decimal("198.00")
