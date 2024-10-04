# c:/Users/fabri/Repos/flexup/flexup-backend/payment_term/models.py

import math
from django.db import models
from decimal import Decimal as Dec

from django.forms import ValidationError

from core.enums.helpers import FlexUpEnum
from core.enums.status import Status

from .enums import Priority,Period,  StartDate, PrimaryAdjustment, TokenRedemption
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _
from core.enums.general import Focus
from uuid import uuid4 as uuid  # Fab→Fahad 2024-10-03: why don't we use uuids ?

class Commitment(models.Model):
    tranche = models.ForeignKey("tranche.Tranche",on_delete=models.PROTECT, related_name="commitments",related_query_name="commitment")
    iteration = models.PositiveIntegerField(default=1)
    priority = models.CharField(max_length=1, choices=Priority.filter_by('period'))
    principal = models.DecimalField(max_digits=15, decimal_places=2)
    payor_account = models.ForeignKey("accounts.Account",on_delete=models.PROTECT, related_name="commitments_as_payor",related_query_name="commitment_as_payor", default=tranche.payor_account)
    payee_account = models.ForeignKey("accounts.Account",on_delete=models.PROTECT, related_name="commitments_as_payee",related_query_name="commitment_as_payee", default=tranche.payee_account)
    focus = models.CharField(max_length=1, choices=Focus.choices())
    status = models.CharField(max_length=1, choices=Status.choices()) # Fab→Fahad 2024-10-03: need to fix the status subclass before I can develop the business logic here