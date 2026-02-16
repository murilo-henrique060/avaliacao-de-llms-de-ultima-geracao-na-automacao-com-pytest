
"""
Automated tests for E-commerce Order System
Based on formal specifications - Business Rules (BR) and Functional Requirements (FR)
"""

import pytest
from decimal import Decimal
from cases.case02 import Item, Order


# =============================================================================
# BR01 – An order must contain at least one item
# =============================================================================

class TestBR01OrderMustContainAtLeastOneItem: 
    
    def test_order_with_one_item_is_valid(self):
        # BR01 – An order must contain at least one item
        order = Order()
        item = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        order.add_item(item)
        # Order with one item should be valid and calculate total successfully
        total = order.calculate_total()
        assert total == Decimal("50.00")
    
    def test_order_with_no_items_raises_exception(self):
        # BR01 – An order must contain at least one item
        order = Order()
        with pytest.raises(Exception):
            order.calculate_total()


# =============================================================================
# BR02 – Each item must have a minimum quantity of 1
# =============================================================================

class TestBR02ItemMinimumQuantity:
    
    def test_item_with_quantity_one_is_valid(self):
        # BR02 – Each item must have a minimum quantity of 1
        order = Order()
        item = Item(name="Product A", price=Decimal("100.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("100.00")
    
    def test_item_with_quantity_zero_raises_exception(self):
        # BR02 – Each item must have a minimum quantity of 1
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("100.00"), quantity=0)
    
    def test_item_with_negative_quantity_raises_exception(self):
        # BR02 – Each item must have a minimum quantity of 1
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("100.00"), quantity=-1)


# =============================================================================
# BR03 – All items must have a positive price
# =============================================================================

class TestBR03ItemPositivePrice:
    
    def test_item_with_positive_price_is_valid(self):
        # BR03 – All items must have a positive price
        order = Order()
        item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("0.01")
    
    def test_item_with_zero_price_raises_exception(self):
        # BR03 – All items must have a positive price
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("0.00"), quantity=1)
    
    def test_item_with_negative_price_raises_exception(self):
        # BR03 – All items must have a positive price
        with pytest. raises(Exception):
            Item(name="Product A", price=Decimal("-10.00"), quantity=1)


# =============================================================================
# BR04 – The total order value is the sum of the items
# =============================================================================

class TestBR04TotalOrderValueCalculation:
    
    def test_total_with_single_item_single_quantity(self):
        # BR04 – The total order value is the sum of the items
        order = Order()
        item = Item(name="Product A", price=Decimal("75.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("75.00")
    
    def test_total_with_single_item_multiple_quantity(self):
        # BR04 – The total order value is the sum of the items
        order = Order()
        item = Item(name="Product A", price=Decimal("25.00"), quantity=3)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("75.00")
    
    def test_total_with_multiple_items(self):
        # BR04 – The total order value is the sum of the items
        order = Order()
        item1 = Item(name="Product A", price=Decimal("30.00"), quantity=2)
        item2 = Item(name="Product B", price=Decimal("50.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order. calculate_total()
        # (30.00 * 2) + (50.00 * 1) = 60.00 + 50.00 = 110.00
        assert total == Decimal("110.00")
    
    def test_total_with_three_items_various_quantities(self):
        # BR04 – The total order value is the sum of the items
        order = Order()
        item1 = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("20.00"), quantity=2)
        item3 = Item(name="Product C", price=Decimal("15.00"), quantity=3)
        order.add_item(item1)
        order.add_item(item2)
        order.add_item(item3)
        total = order.calculate_total()
        # (10.00 * 1) + (20.00 * 2) + (15.00 * 3) = 10.00 + 40.00 + 45.00 = 95.00
        assert total == Decimal("95.00")


# =============================================================================
# BR05 – Orders above R$ 200 receive a 10% discount
# =============================================================================

class TestBR05DiscountForOrdersAbove200:
    
    def test_order_exactly_200_does_not_receive_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount
        order = Order()
        item = Item(name="Product A", price=Decimal("200.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # Exactly R$ 200.00 does not qualify for discount
        assert total == Decimal("200.00")
    
    def test_order_above_200_receives_10_percent_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount
        order = Order()
        item = Item(name="Product A", price=Decimal("200.01"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 200.01 - 10% = 200.01 * 0.90 = 180.009
        assert total == Decimal("180.009")
    
    def test_order_below_200_does_not_receive_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount
        order = Order()
        item = Item(name="Product A", price=Decimal("199.99"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # Below R$ 200.00 does not qualify for discount
        assert total == Decimal("199.99")
    
    def test_order_300_receives_10_percent_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount
        order = Order()
        item = Item(name="Product A", price=Decimal("300.00"), quantity=1)
        order.add_item(item)
        total = order. calculate_total()
        # 300.00 - 10% = 300.00 * 0.90 = 270.00
        assert total == Decimal("270.00")


# =============================================================================
# BR06 – The discount must not be applied more than once
# =============================================================================

class TestBR06DiscountAppliedOnlyOnce: 
    
    def test_calling_calculate_total_twice_applies_discount_only_once(self):
        # BR06 – The discount must not be applied more than once
        order = Order()
        item = Item(name="Product A", price=Decimal("250.00"), quantity=1)
        order.add_item(item)
        # First call
        total1 = order.calculate_total()
        # Second call
        total2 = order.calculate_total()
        # 250.00 - 10% = 225.00 (discount applied only once, not compounded)
        assert total1 == Decimal("225.00")
        assert total2 == Decimal("225.00")
    
    def test_calling_calculate_total_multiple_times_returns_consistent_result(self):
        # BR06 – The discount must not be applied more than once
        order = Order()
        item = Item(name="Product A", price=Decimal("400.00"), quantity=1)
        order.add_item(item)
        # Multiple calls
        total1 = order.calculate_total()
        total2 = order.calculate_total()
        total3 = order. calculate_total()
        # 400.00 - 10% = 360.00 (consistent across all calls)
        expected = Decimal("360.00")
        assert total1 == expected
        assert total2 == expected
        assert total3 == expected


# =============================================================================
# FR01 – Create an order with multiple items
# =============================================================================

class TestFR01CreateOrderWithMultipleItems:
    
    def test_create_order_with_two_items(self):
        # FR01 – Create an order with multiple items
        order = Order()
        item1 = Item(name="Product A", price=Decimal("25.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("35.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order.calculate_total()
        assert total == Decimal("60.00")
    
    def test_create_order_with_five_items(self):
        # FR01 – Create an order with multiple items
        order = Order()
        item1 = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("20.00"), quantity=1)
        item3 = Item(name="Product C", price=Decimal("30.00"), quantity=1)
        item4 = Item(name="Product D", price=Decimal("40.00"), quantity=1)
        item5 = Item(name="Product E", price=Decimal("50.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        order.add_item(item3)
        order.add_item(item4)
        order.add_item(item5)
        total = order.calculate_total()
        # 10 + 20 + 30 + 40 + 50 = 150.00
        assert total == Decimal("150.00")


# =============================================================================
# FR02 – Correctly calculate the total
# =============================================================================

class TestFR02CorrectlyCalculateTotal: 
    
    def test_calculate_total_with_decimal_prices(self):
        # FR02 – Correctly calculate the total
        order = Order()
        item1 = Item(name="Product A", price=Decimal("19.99"), quantity=2)
        item2 = Item(name="Product B", price=Decimal("5.50"), quantity=3)
        order.add_item(item1)
        order.add_item(item2)
        total = order.calculate_total()
        # (19.99 * 2) + (5.50 * 3) = 39.98 + 16.50 = 56.48
        assert total == Decimal("56.48")
    
    def test_calculate_total_preserves_decimal_precision(self):
        # FR02 – Correctly calculate the total
        order = Order()
        item = Item(name="Product A", price=Decimal("33.33"), quantity=3)
        order.add_item(item)
        total = order.calculate_total()
        # 33.33 * 3 = 99.99
        assert total == Decimal("99.99")


# =============================================================================
# FR03 – The system must apply the discount correctly when eligible
# =============================================================================

class TestFR03ApplyDiscountCorrectlyWhenEligible:
    
    def test_discount_applied_correctly_for_order_of_500(self):
        # FR03 – The system must apply the discount correctly when eligible
        order = Order()
        item = Item(name="Product A", price=Decimal("500.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 500.00 - 10% = 450.00
        assert total == Decimal("450.00")
    
    def test_discount_not_applied_for_order_of_150(self):
        # FR03 – The system must apply the discount correctly when eligible
        order = Order()
        item = Item(name="Product A", price=Decimal("150.00"), quantity=1)
        order.add_item(item)
        total = order. calculate_total()
        # Below R$ 200.00, no discount
        assert total == Decimal("150.00")
    
    def test_discount_applied_for_multiple_items_totaling_above_200(self):
        # FR03 – The system must apply the discount correctly when eligible
        order = Order()
        item1 = Item(name="Product A", price=Decimal("80.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("70.00"), quantity=1)
        item3 = Item(name="Product C", price=Decimal("60.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        order.add_item(item3)
        total = order.calculate_total()
        # 80 + 70 + 60 = 210.00, above 200 so 10% discount
        # 210.00 * 0.90 = 189.00
        assert total == Decimal("189.00")


# =============================================================================
# FR04 – The system must display the final order value
# =============================================================================

class TestFR04DisplayFinalOrderValue:
    
    def test_calculate_total_returns_final_value_without_discount(self):
        # FR04 – The system must display the final order value
        order = Order()
        item = Item(name="Product A", price=Decimal("100.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # Final value is returned (no discount for orders <= 200)
        assert total == Decimal("100.00")
    
    def test_calculate_total_returns_final_value_with_discount(self):
        # FR04 – The system must display the final order value
        order = Order()
        item = Item(name="Product A", price=Decimal("250.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # Final value after discount:  250.00 * 0.90 = 225.00
        assert total == Decimal("225.00")


# =============================================================================
# FR05 – The system must raise an exception in case of a failure
# =============================================================================

class TestFR05RaiseExceptionOnFailure:
    
    def test_exception_raised_for_empty_order(self):
        # FR05 – The system must raise an exception in case of a failure
        order = Order()
        with pytest.raises(Exception):
            order.calculate_total()
    
    def test_exception_raised_for_item_with_zero_quantity(self):
        # FR05 – The system must raise an exception in case of a failure
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("50.00"), quantity=0)
    
    def test_exception_raised_for_item_with_negative_quantity(self):
        # FR05 – The system must raise an exception in case of a failure
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("50.00"), quantity=-5)
    
    def test_exception_raised_for_item_with_zero_price(self):
        # FR05 – The system must raise an exception in case of a failure
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("0.00"), quantity=1)
    
    def test_exception_raised_for_item_with_negative_price(self):
        # FR05 – The system must raise an exception in case of a failure
        with pytest. raises(Exception):
            Item(name="Product A", price=Decimal("-25.00"), quantity=1)


# =============================================================================
# Edge Cases – Explicitly required by the rules
# =============================================================================

class TestEdgeCases:
    
    def test_order_total_exactly_at_discount_boundary_200(self):
        # Edge case for BR05 – boundary value exactly at R$ 200.00
        order = Order()
        item = Item(name="Product A", price=Decimal("100.00"), quantity=2)
        order.add_item(item)
        total = order.calculate_total()
        # Exactly 200.00 - no discount per BR05 (must be ABOVE 200)
        assert total == Decimal("200.00")
    
    def test_order_total_just_above_discount_boundary(self):
        # Edge case for BR05 – boundary value just above R$ 200.00
        order = Order()
        item = Item(name="Product A", price=Decimal("100.01"), quantity=2)
        order.add_item(item)
        total = order.calculate_total()
        # 200.02 is above 200, so 10% discount:  200.02 * 0.90 = 180.018
        assert total == Decimal("180.018")
    
    def test_item_with_minimum_valid_quantity(self):
        # Edge case for BR02 – minimum valid quantity is 1
        order = Order()
        item = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("50.00")
    
    def test_item_with_minimum_valid_positive_price(self):
        # Edge case for BR03 – minimum valid positive price
        order = Order()
        item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("0.01")
    
    def test_order_with_single_item_minimum_valid_values(self):
        # Edge case for BR01, BR02, BR03 – order with minimum valid values
        order = Order()
        item = Item(name="Product A", price=Decimal("0.01"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("0.01")
