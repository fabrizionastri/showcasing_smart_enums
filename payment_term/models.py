from decimal import Decimal
from email.policy import default
from tokenize import blank_re

from django.db import models

from .enums import Priority,Period,  StartDate, PrimaryAdjustment, TokenRedemption
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from uuid import uuid4 as uuid



class PaymentTermTemplate(models.Model):
    """
    Payment terms templates are uniquely defined by their code, which is a concatenation of their parameters.
    System templates have a name. User generated template have their short label as a name. User generated templates
    are not editable and are pooled, meaning that once a user generated template is created, it is available to all users.
    A popularity indicator tracks the number of times a user generated template has been used (log of the number of times, not in MVP).
    """
    # System templates
    name = models.CharField(max_length=255, unique=True)
    is_system = models.BooleanField(default=True)

    # Primary commitment parameters
    primary_priority = models.CharField(max_length=1,choices=Priority.choices_with_property('primary_rf'))
    primary_start = models.CharField(max_length=1,choices=StartDate.choices_with_property('primary_rf'), default=StartDate.DELIVERY_FINISH.value)
    primary_period = models.CharField(max_length=1,choices=Period.filtered_choices(Period.YEAR, Period.QUARTER, Period.MONTH, Period.WEEK, Period.DAY), default=Period.MONTH.value, blank=True)
    primary_offset = models.IntegerField(default=1)
    primary_adjustment = models.CharField(max_length=1,choices=PrimaryAdjustment.all_choices, default=PrimaryAdjustment.EOP.value)

    # Interest parameters
    interest_rate = models.DecimalField(max_digits=4,decimal_places=2, default=Decimal('0'),validators=[MinValueValidator(Decimal('0')),MaxValueValidator(Decimal('50'))])
    interest_priority = models.CharField(max_length=1,choices=Priority.choices_with_property('interest_rf'), default=Priority.NA.value)
    interest_start = models.CharField(max_length=1,choices=StartDate.choices_with_property('interest_rf'), default=StartDate.NA.value)
    interest_period = models.CharField(max_length=1,choices=Period.choices_with_property('interest_rf'), default=Period.NA.value)

    # Residue parameters
    residue_priority = models.CharField(max_length=1,choices=Priority.choices_with_property('residue_rf'), default=Priority.NA.value)
    residue_period = models.CharField(max_length=1,choices=Period.choices_with_property('residue_rf'), default=Period.MONTH.value)

    # Token redemption parameters
    token_redemption = models.CharField(max_length=1,choices=TokenRedemption.all_choices, default=TokenRedemption.NO.value)

    # Summary of payment terms, to be used in tables and lists
    @property
    def code(self):
        # the code is the contatenation of of all the parameters above
        return f"{self.primary_priority.value}{self.primary_start.value}{self.primary_period.value}{self.primary_offset}{self.primary_adjustment.value}-{self.interest_rate}{self.interest_priority.value}{self.interest_start.value}{self.interest_period.value}-{self.residue_priority.value}{self.residue_period.value}-{self.token_redemption.value}"

    @property
    def priority_label(self):
        return f"{self.primary_priority.label}"

    @property
    def due_date_label(self):
        return f"{self.primary_offset}{self.primary_period.label.lower()}(s) from {self.primary_start.label}{", " + self.primary_adjustment.short_name}"

    @property
    def interest_label(self):
        return f"{self.interest_rate}% {self.interest_priority.label.lower()}, {self.interest_period.periodicity.lower()} starting on {self.interest_start.label.lower()}"

    @property
    def residue_label(self):
        return f"{self.residue_priority.label.lower()} {self.residue_period.periodicity.lower()}"

    @property
    def redeemable_label(self):
        return self.token_redemption.label.capitalize()

    @property
    def label(self):
        return ("System: " if self.is_system else "Custom: ") + self.priority_label + ", " + self.due_date_label + ", " + self.interest_label + ", " + self.residue_label + ", " + self.redeemable_label

    # Short summary of payment terms
    @property
    def priority_short_label(self):
        return f"{self.primary_priority.short_name}"

    @property
    def due_date_short_label(self):

        return f"{self.primary_start.short_name}+{self.primary_offset}{self.primary_period.value} {self.primary_adjustment.short_name}"

    @property
    def interest_short_label(self):
        return f"{self.interest_rate}% {self.interest_priority.short_name} {self.interest_period.short_name} from {self.interest_start.short_name}"

    @property
    def residue_short_label(self):
        return f"{self.residue_priority.short_name} {self.residue_period.short_name}"

    @property
    def redeemable_short_label(self):
        return self.token_redemption.short_name

    @property
    def short_label(self):
        return  ("S: " if self.is_system else "C: ") + self.priority_short_label + ", " + self.due_date_short_label + ", " + self.interest_short_label + ", " + self.residue_short_label + ", " + self.redeemable_short_label

    def __str__(self):
        return self.name

    from django.db import models

class PaymentTerm(models.Model):
    # Payment terms
    id = models.CharField(max_length=255, unique=True, default=uuid, editable=False, primary_key=True)
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"), blank=True)
    templates = models.ManyToManyField(PaymentTermTemplate, verbose_name=_("Templates"), related_name="payment_terms")
    is_active = models.BooleanField(default=True, verbose_name=_("Is active"))

    class Meta:
        verbose_name = _("Payment term")
        verbose_name_plural = _("Payment terms")

    def __str__(self):
        return self.name