
"""
Automated tests for E-commerce Order System
Based exclusively on provided Business Rules (BR) and Functional Requirements (FR)
"""

import pytest
from decimal import Decimal

# Import the classes to be tested (assuming they exist in a module called 'order_system')
from cases.case02 import Item, Order


class TestBR01OrderMustContainAtLeastOneItem:
    """Tests for BR01: An order must contain at least one item"""

    def test_order_with_no_items_raises_exception(self):
        # BR01 – An order must contain at least one item
        order = Order()
        with pytest.raises(Exception):
            order.calculate_total()

    def test_order_with_one_item_is_valid(self):
        # BR01 – An order must contain at least one item (positive case)
        order = Order()
        item = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("50.00")


class TestBR02EachItemMustHaveMinimumQuantityOfOne:
    """Tests for BR02: Each item must have a minimum quantity of 1"""

    def test_item_with_quantity_zero_raises_exception(self):
        # BR02 – Each item must have a minimum quantity of 1
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=0)

    def test_item_with_negative_quantity_raises_exception(self):
        # BR02 – Each item must have a minimum quantity of 1
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=-1)

    def test_item_with_quantity_one_is_valid(self):
        # BR02 – Each item must have a minimum quantity of 1 (positive case)
        item = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        assert item.quantity == 1

    def test_item_with_quantity_greater_than_one_is_valid(self):
        # BR02 – Each item must have a minimum quantity of 1 (positive case)
        item = Item(name="Product A", price=Decimal("10.00"), quantity=5)
        assert item.quantity == 5


class TestBR03AllItemsMustHavePositivePrice:
    """Tests for BR03: All items must have a positive price"""

    def test_item_with_zero_price_raises_exception(self):
        # BR03 – All items must have a positive price
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("0.00"), quantity=1)

    def test_item_with_negative_price_raises_exception(self):
        # BR03 – All items must have a positive price
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("-10.00"), quantity=1)

    def test_item_with_positive_price_is_valid(self):
        # BR03 – All items must have a positive price (positive case)
        item = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        assert item.price == Decimal("10.00")


class TestBR04TotalOrderValueIsSumOfItems: 
    """Tests for BR04: The total order value is the sum of the items"""

    def test_total_with_single_item_quantity_one(self):
        # BR04 – The total order value is the sum of the items
        order = Order()
        item = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("50.00")

    def test_total_with_single_item_quantity_multiple(self):
        # BR04 – The total order value is the sum of the items
        order = Order()
        item = Item(name="Product A", price=Decimal("25.00"), quantity=4)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("100.00")

    def test_total_with_multiple_items(self):
        # BR04 – The total order value is the sum of the items
        order = Order()
        item1 = Item(name="Product A", price=Decimal("30.00"), quantity=2)
        item2 = Item(name="Product B", price=Decimal("20.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order. calculate_total()
        # (30.00 * 2) + (20.00 * 1) = 60.00 + 20.00 = 80.00
        assert total == Decimal("80.00")

    def test_total_with_three_different_items(self):
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


class TestBR05OrdersAbove200ReceiveTenPercentDiscount:
    """Tests for BR05: Orders above R$ 200 receive a 10% discount"""

    def test_order_exactly_200_does_not_receive_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount (edge case:  exactly 200)
        order = Order()
        item = Item(name="Product A", price=Decimal("200.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("200.00")

    def test_order_below_200_does_not_receive_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount (below threshold)
        order = Order()
        item = Item(name="Product A", price=Decimal("199.99"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("199.99")

    def test_order_above_200_receives_ten_percent_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount
        order = Order()
        item = Item(name="Product A", price=Decimal("200.01"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 200.01 - 10% = 200.01 * 0.90 = 180.009
        assert total == Decimal("180.009")

    def test_order_300_receives_ten_percent_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount
        order = Order()
        item = Item(name="Product A", price=Decimal("300.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 300.00 - 10% = 300.00 * 0.90 = 270.00
        assert total == Decimal("270.00")

    def test_order_with_multiple_items_above_200_receives_discount(self):
        # BR05 – Orders above R$ 200 receive a 10% discount
        order = Order()
        item1 = Item(name="Product A", price=Decimal("150.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("100.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order.calculate_total()
        # (150.00 + 100.00) = 250.00 > 200, so 250.00 * 0.90 = 225.00
        assert total == Decimal("225.00")


class TestBR06DiscountMustNotBeAppliedMoreThanOnce:
    """Tests for BR06: The discount must not be applied more than once"""

    def test_discount_applied_only_once_on_multiple_calculate_total_calls(self):
        # BR06 – The discount must not be applied more than once
        order = Order()
        item = Item(name="Product A", price=Decimal("300.00"), quantity=1)
        order.add_item(item)
        first_total = order. calculate_total()
        second_total = order. calculate_total()
        third_total = order. calculate_total()
        # All calls should return the same value:  300.00 * 0.90 = 270.00
        assert first_total == Decimal("270.00")
        assert second_total == Decimal("270.00")
        assert third_total == Decimal("270.00")

    def test_discount_consistency_after_multiple_calculations(self):
        # BR06 – The discount must not be applied more than once
        order = Order()
        item = Item(name="Product A", price=Decimal("400.00"), quantity=1)
        order.add_item(item)
        first_total = order. calculate_total()
        second_total = order.calculate_total()
        # Both should be 400.00 * 0.90 = 360.00
        assert first_total == second_total == Decimal("360.00")


class TestFR01CreateOrderWithMultipleItems: 
    """Tests for FR01: Create an order with multiple items"""

    def test_create_order_with_two_items(self):
        # FR01 – Create an order with multiple items
        order = Order()
        item1 = Item(name="Product A", price=Decimal("25.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("35.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        total = order. calculate_total()
        assert total == Decimal("60.00")

    def test_create_order_with_five_items(self):
        # FR01 – Create an order with multiple items
        order = Order()
        item1 = Item(name="Product A", price=Decimal("10.00"), quantity=1)
        item2 = Item(name="Product B", price=Decimal("20.00"), quantity=1)
        item3 = Item(name="Product C", price=Decimal("30.00"), quantity=1)
        item4 = Item(name="Product D", price=Decimal("15.00"), quantity=1)
        item5 = Item(name="Product E", price=Decimal("25.00"), quantity=1)
        order.add_item(item1)
        order.add_item(item2)
        order.add_item(item3)
        order.add_item(item4)
        order.add_item(item5)
        total = order.calculate_total()
        # 10 + 20 + 30 + 15 + 25 = 100.00
        assert total == Decimal("100.00")


class TestFR02CorrectlyCalculateTotal:
    """Tests for FR02: Correctly calculate the total"""

    def test_calculate_total_single_item_single_quantity(self):
        # FR02 – Correctly calculate the total
        order = Order()
        item = Item(name="Product A", price=Decimal("75.50"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("75.50")

    def test_calculate_total_single_item_multiple_quantity(self):
        # FR02 – Correctly calculate the total
        order = Order()
        item = Item(name="Product A", price=Decimal("33.33"), quantity=3)
        order.add_item(item)
        total = order.calculate_total()
        # 33.33 * 3 = 99.99
        assert total == Decimal("99.99")

    def test_calculate_total_multiple_items_varying_quantities(self):
        # FR02 – Correctly calculate the total
        order = Order()
        item1 = Item(name="Product A", price=Decimal("12.50"), quantity=2)
        item2 = Item(name="Product B", price=Decimal("7.25"), quantity=4)
        order.add_item(item1)
        order.add_item(item2)
        total = order. calculate_total()
        # (12.50 * 2) + (7.25 * 4) = 25.00 + 29.00 = 54.00
        assert total == Decimal("54.00")


class TestFR03ApplyDiscountCorrectlyWhenEligible:
    """Tests for FR03: The system must apply the discount correctly when eligible"""

    def test_discount_applied_correctly_when_total_exceeds_200(self):
        # FR03 – The system must apply the discount correctly when eligible
        order = Order()
        item = Item(name="Product A", price=Decimal("250.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 250.00 * 0.90 = 225.00
        assert total == Decimal("225.00")

    def test_no_discount_applied_when_total_does_not_exceed_200(self):
        # FR03 – The system must apply the discount correctly when eligible (negative case)
        order = Order()
        item = Item(name="Product A", price=Decimal("150.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert total == Decimal("150.00")

    def test_discount_calculation_precision(self):
        # FR03 – The system must apply the discount correctly when eligible
        order = Order()
        item = Item(name="Product A", price=Decimal("201.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 201.00 * 0.90 = 180.90
        assert total == Decimal("180.90")


class TestFR04DisplayFinalOrderValue: 
    """Tests for FR04: The system must display the final order value"""

    def test_final_value_returned_without_discount(self):
        # FR04 – The system must display the final order value
        order = Order()
        item = Item(name="Product A", price=Decimal("100.00"), quantity=1)
        order.add_item(item)
        total = order. calculate_total()
        assert total == Decimal("100.00")

    def test_final_value_returned_with_discount(self):
        # FR04 – The system must display the final order value
        order = Order()
        item = Item(name="Product A", price=Decimal("500.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        # 500.00 * 0.90 = 450.00
        assert total == Decimal("450.00")

    def test_final_value_is_decimal_type(self):
        # FR04 – The system must display the final order value
        order = Order()
        item = Item(name="Product A", price=Decimal("50.00"), quantity=1)
        order.add_item(item)
        total = order.calculate_total()
        assert isinstance(total, Decimal)


class TestFR05RaiseExceptionOnFailure:
    """Tests for FR05: The system must raise an exception in case of a failure"""

    def test_exception_raised_for_empty_order(self):
        # FR05 – The system must raise an exception in case of a failure
        order = Order()
        with pytest.raises(Exception):
            order. calculate_total()

    def test_exception_raised_for_invalid_item_quantity(self):
        # FR05 – The system must raise an exception in case of a failure
        with pytest.raises(Exception):
            Item(name="Product A", price=Decimal("10.00"), quantity=0)

    def test_exception_raised_for_invalid_item_price(self):
        # FR05 – The system must raise an exception in case of a failure
        with pytest. raises(Exception):
            Item(name="Product A", price=Decimal("-5.00"), quantity=1)

    def test_exception_raised_for_zero_price(self):
        # FR05 – The system must raise an exception in case of a failure
        with pytest. raises(Exception):
            Item(name="Product A", price=Decimal("0.00"), quantity=1)
