import unittest
from django.test import TestCase
from decimal import Decimal as Dec
from .enums import Period, Priority, StartDate, PrimaryAdjustment, TokenRedemption


class TestFlexUpEnum(TestCase):

    def test_choices(self):
        self.assertEqual(
            Period.all_choices(),
            [
                ('Y', 'Year'),
                ('Q', 'Quarter'),
                ('M', 'Month'),
                ('W', 'Week'),
                ('D', 'Day'),
                ('A', 'Same as primary'),
                ('N', 'Not applicable')
            ]
        )
        self.assertEqual(
            Priority.all_choices(),
            [
                ('R', 'Firm'),
                ('P', 'Preferred'),
                ('F', 'Flex'),
                ('S', 'Superflex'),
                ('C', 'Credit'),
                ('T', 'Token'),
                ('A', 'Same as primary'),
                ('D', 'Distribution')
            ]
        )
        self.assertEqual(
            StartDate.all_choices(),
            [
                ('O', 'Order confirmation date'),
                ('S', 'Delivery start date'),
                ('M', 'Delivery middle date'),
                ('F', 'Delivery finish date'),
                ('D', 'Intial due date'),
                ('N', 'Not applicable')
            ]
        )
        self.assertEqual(
            PrimaryAdjustment.all_choices(),
            [
                ('B', 'Beginning of period'),
                ('E', 'End of period'),
                ('N', 'No adjustment')
            ]
        )
        self.assertEqual(
            TokenRedemption.all_choices(),
            [
                ('Y', 'Redeemable tokens'),
                ('N', 'Non-redeemable tokens')
            ]
        )


    def test_limited_choices(self):
        self.assertEqual(
            Period.filtered_choices('YEAR', 'MONTH'),
            [
                ('Y', 'Year'),
                ('M', 'Month')
            ]
        )
        self.assertEqual(
            Priority.filtered_choices('FIRM', 'FLEX'),
            [
                ('R', 'Firm'),
                ('F', 'Flex')
            ]
        )
    # this is another way of writing the test above
    def test_period_limited_choices(self):
        selected = ['YEAR', 'MONTH']
        expected = [('Y', ('Year')),('M', ('Month')) ]
        actual = Period.filtered_choices(*selected)
        self.assertCountEqual(actual, expected)

    def test_choices_for(self):
        self.assertEqual(
            Period.choices_with_property('interest_rf'),
            [
                ('Y', 'Year'),
                ('Q', 'Quarter'),
                ('M', 'Month'),
                ('A', 'Same as primary'),
                ('N', 'Not applicable')
            ]
        )
        self.assertEqual(
            Priority.choices_with_property('special'),
            [
                (Priority.DISTRIBUTION.value, Priority.DISTRIBUTION.label)
            ]
        )
        self.assertEqual(
            Priority.choices_with_property('special'),
            [
                ('D', 'Distribution')
            ]
        )
        # user
        self.assertCountEqual(
            Priority.choices_with_property('interest_level'),
            [
                ('R', 'Firm'),
                ('P', 'Preferred'),
                ('F', 'Flex'),
                ('S', 'Superflex'),
                ('C', 'Credit')
            ]
        )

if __name__ == '__main__':
    unittest.main()