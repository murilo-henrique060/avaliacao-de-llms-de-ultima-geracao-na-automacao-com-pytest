
import pytest
from decimal import Decimal

# Assuming the classes Item and Order are imported from the system module
# from system.ecommerce import Item, Order

# Since the system implementation is not provided, we mock the expected behavior 
# for the purpose of generating the test file structure. 
# In a real scenario, these imports would point to the actual source code.

from cases.case02 import Item, Order  # type: ignore

class TestEcommerceOrderSystem:

    # ==========================================================================
    # BR01: An order must contain at least one item
    # ==========================================================================
    
    def test_br01_validation_error_empty_order(self):
        # FR05 – The system must raise an exception in case of a failure
        # BR01 – An order must contain at least one item
        order = Order()
        
        # Expectation: Calculating total on an empty order raises an exception
        # strictly enforcing the rule that an order must have items.
        with pytest.raises(Exception):
            order.calculate_total()

    # ==========================================================================
    # BR02: Each item must have a minimum quantity of 1
    # ==========================================================================

    def test_br02_validation_error_quantity_zero(self):
        # FR05 – The system must raise an exception in case of a failure
        # BR02 – Each item must have a minimum quantity of 1
        
        # Expectation: Instantiating an item with quantity 0 raises an exception.
        with pytest.raises(Exception):
            Item(name="Mouse", price=Decimal("50.00"), quantity=0)

    def test_br02_validation_error_quantity_negative(self):
        # FR05 – The system must raise an exception in case of a failure
        # BR02 – Each item must have a minimum quantity of 1
        
        # Expectation: Instantiating an item with negative quantity raises an exception.
        with pytest.raises(Exception):
            Item(name="Mouse", price=Decimal("50.00"), quantity=-1)

    def test_br02_valid_quantity_one(self):
        # BR02 – Each item must have a minimum quantity of 1
        # Validates boundary condition where quantity is exactly 1 (valid).
        item = Item(name="Mouse", price=Decimal("50.00"), quantity=1)
        assert item.quantity == 1

    # ==========================================================================
    # BR03: All items must have a positive price
    # ==========================================================================

    def test_br03_validation_error_price_zero(self):
        # FR05 – The system must raise an exception in case of a failure
        # BR03 – All items must have a positive price
        
        # Expectation: Instantiating an item with price 0.00 raises an exception.
        with pytest.raises(Exception):
            Item(name="Free Gift", price=Decimal("0.00"), quantity=1)

    def test_br03_validation_error_price_negative(self):
        # FR05 – The system must raise an exception in case of a failure
        # BR03 – All items must have a positive price
        
        # Expectation: Instantiating an item with negative price raises an exception.
        with pytest.raises(Exception):
            Item(name="Refund", price=Decimal("-10.00"), quantity=1)

    def test_br03_valid_positive_price(self):
        # BR03 – All items must have a positive price
        # Validates a standard positive price.
        item = Item(name="Keyboard", price=Decimal("0.01"), quantity=1)
        assert item.price == Decimal("0.01")

    # ==========================================================================
    # BR04: The total order value is the sum of the items
    # FR02: Correctly calculate the total
    # FR04: The system must display the final order value
    # ==========================================================================

    def test_br04_fr02_calculate_simple_sum(self):
        # BR04 – The total order value is the sum of the items
        # FR02 – Correctly calculate the total
        # FR04 – The system must display the final order value
        
        # Scenario: Total is below discount threshold (R$ 200).
        # Item 1: 50.00 * 2 = 100.00
        # Item 2: 30.00 * 1 = 30.00
        # Total expected: 130.00
        
        order = Order()
        item1 = Item(name="Item A", price=Decimal("50.00"), quantity=2)
        item2 = Item(name="Item B", price=Decimal("30.00"), quantity=1)
        
        order.add_item(item1)
        order.add_item(item2)
        
        total = order.calculate_total()
        assert total == Decimal("130.00")

    # ==========================================================================
    # BR05: Orders above R$ 200 receive a 10% discount
    # FR03: The system must apply the discount correctly when eligible
    # ==========================================================================

    def test_br05_boundary_exact_200_no_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount (Strictly > 200)
        # FR02 – Correctly calculate the total
        
        # Scenario: Total is exactly R$ 200.00.
        # Rule says "above", so 200 does not qualify.
        # Expected: 200.00
        
        order = Order()
        item = Item(name="Expensive Item", price=Decimal("200.00"), quantity=1)
        order.add_item(item)
        
        total = order.calculate_total()
        assert total == Decimal("200.00")

    def test_br05_fr03_boundary_200_01_applies_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount
        # FR03 – The system must apply the discount correctly when eligible
        
        # Scenario: Total is R$ 200.01 (Just above threshold).
        # Calculation: 200.01 - 10% = 200.01 * 0.90
        # 200.01 * 0.9 = 180.009
        # Assuming standard currency handling, but adhering to constraints not to assume rounding,
        # we assert the exact Decimal result of the multiplication.
        
        order = Order()
        item = Item(name="Just Above", price=Decimal("200.01"), quantity=1)
        order.add_item(item)
        
        total = order.calculate_total()
        expected = Decimal("200.01") * Decimal("0.90")
        assert total == expected

    def test_br05_fr03_large_value_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount
        # FR03 – The system must apply the discount correctly when eligible
        
        # Scenario: Total is 300.00.
        # Expected: 300.00 * 0.90 = 270.00
        
        order = Order()
        item = Item(name="Very Expensive", price=Decimal("100.00"), quantity=3)
        order.add_item(item)
        
        total = order.calculate_total()
        assert total == Decimal("270.00")

    # ==========================================================================
    # BR06: The discount must not be applied more than once
    # ==========================================================================

    def test_br06_idempotency_calculate_total(self):
        # BR06 – The discount must not be applied more than once
        
        # Scenario: Calculate total multiple times on the same order.
        # The result must remain consistent and not apply 10% recursively.
        # Base: 300.00 -> Discounted: 270.00
        
        order = Order()
        item = Item(name="Item", price=Decimal("300.00"), quantity=1)
        order.add_item(item)
        
        first_calculation = order.calculate_total()
        second_calculation = order.calculate_total()
        
        assert first_calculation == Decimal("270.00")
        assert second_calculation == Decimal("270.00")

    # ==========================================================================
    # FR01: Create an order with multiple items
    # ==========================================================================

    def test_fr01_create_order_multiple_distinct_items(self):
        # FR01 – Create an order with multiple items
        # BR04 – The total order value is the sum of the items
        
        # Scenario: Add 3 different items to the order.
        # 1. 10.00 * 1
        # 2. 20.00 * 2
        # 3. 5.00 * 1
        # Sum: 10 + 40 + 5 = 55.00 (No discount)
        
        order = Order()
        order.add_item(Item(name="A", price=Decimal("10.00"), quantity=1))
        order.add_item(Item(name="B", price=Decimal("20.00"), quantity=2))
        order.add_item(Item(name="C", price=Decimal("5.00"), quantity=1))
        
        assert order.calculate_total() == Decimal("55.00")
