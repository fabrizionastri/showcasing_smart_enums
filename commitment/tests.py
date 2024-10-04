from django.test import TestCase
from payment_term.models import PaymentTermTemplate
from payment_term.enums import Priority, Period, StartDate, PrimaryAdjustment, TokenRedemption
from decimal import Decimal

class PaymentTermTemplateTestCase(TestCase):
    def setUp(self):
        self.template_credit = PaymentTermTemplate.objects.create(
            name="Credit Template",
            primary_priority=Priority.CREDIT)

        self.template_firm = PaymentTermTemplate.objects.create(
            name="Test Template",
            primary_priority=Priority.FIRM,
            primary_start=StartDate.DELIVERY_FINISH,
            primary_period=Period.WEEK,
            primary_offset=5,
            primary_adjustment=PrimaryAdjustment.BOP,
            interest_rate=Decimal('2.5'),
            interest_priority=Priority.PREFERRED,
            interest_start=StartDate.DELIVERY_FINISH,
            interest_period=Period.QUARTER,
            residue_priority=Priority.SUPERFLEX,
            residue_period=Period.YEAR,
            token_redemption=TokenRedemption.YES
        )

    # assert that the template is created
    def test_template_credit(self):
        print(self.template_firm.primary_start)
        print('code:', self.template_firm.code)
        print('priority_label:', self.template_firm.priority_label)
        print('due_date_label:', self.template_firm.due_date_label)
        print('interest_label:', self.template_firm.interest_label)
        print('residue_label:', self.template_firm.residue_label)
        print('redeemable_label:', self.template_firm.redeemable_label)
        print('label:', self.template_firm.label)
        print('priority_short_label:', self.template_firm.priority_short_label)
        print('due_date_short_label:', self.template_firm.due_date_short_label)
        print('interest_short_label:', self.template_firm.interest_short_label)
        print('residue_short_label:', self.template_firm.residue_short_label)
        print('short_label:', self.template_firm.short_label)

        self.assertEqual(self.template_credit.name, "Credit Template")
        self.assertEqual(self.template_firm.primary_priority, Priority.FIRM)
        self.assertEqual(self.template_firm.primary_start, StartDate.DELIVERY_FINISH)

    # assert that the

    # def test_code(self):
    #     expected_code = "FIRMDELIVERY_FINISHMONTH1NONE-0.0500NANA-NAFIRM-MONTH-NO"
    #     self.assertEqual(self.template.code(), expected_code)

#     def test_residue_short_label(self):
#         expected_label = "firm month"
#         self.assertEqual(self.template.residue_short_label(), expected_label)
#
#     def test_redeemable_label(self):
#         expected_label = "No"
#         self.assertEqual(self.template.redeemable_label(), expected_label)
#
#     def test_due_date_short_label(self):
#         expected_label = "1 month(s) from delivery_finish with no adjustment"
#         self.assertEqual(self.template.due_date_short_label(), expected_label)
#
#     def test_due_date_label(self):
#         expected_label = "1 month(s) from delivery_finish with no adjustment"
#         self.assertEqual(self.template.due_date_label(), expected_label)
#
#     def test_str(self):
#         self.assertEqual(str(self.template), "Test Template")