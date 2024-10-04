from datetime import timezone
from decimal import Decimal
from operator import index
from re import S
from django.db import models
from django.utils.translation import gettext_lazy as _
from core.enums.status import Status
from django.core.validators import MinValueValidator

class TokenRevision(models.Model):
    class Meta:
        verbose_name = _("Token value revision")
        verbose_name_plural = _("Token value revisions")

    charter = models.ForeignKey("charter.Charter", verbose_name=_("Charter"), on_delete=models.PROTECT)
    date = models.DateField(verbose_name=_("Date"))
    old_value = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_("Old value"), Validators=[MinValueValidator(0.001)])
    new_value = models.DecimalField(max_digits=10, decimal_places=3, verbose_name=_("New value"), Validators=[MinValueValidator(0.001)])
    old_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("Old indexing rate"), Validators=[MinValueValidator(0.01)])
    new_rate = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_("New indexing rate"), Validators=[MinValueValidator(0.01)])
    comment = models.TextField(verbose_name=_("Comment"), blank=True, null=True)

    @property
    def change_value(self):
        return (self.new_value - self.old_value) / self.old_value * 100

    @property
    def change_rate(self):
        return (self.new_rate - self.old_rate)

    def __str__(self):
        value_label = ''
        rate_label = ''
        if self.change_value:
            sign = "+" if self.change_value > 0 else "-"
            value_label = f"{self.old_value}→{self.new_value} ({sign}{abs(self.change_value):.2f}%)"
        if self.change_rate:
            sign = "+" if self.new_rate > self.old_rate else "-"
            rate_label = f"{self.old_rate}→{self.new_rate} ({sign}{abs(self.change_rate):.2f}%)"
        return f"{self.date.strftime('%Y-%m-%d')}: {value_label}{', ' if value_label and rate_label else ''}{rate_label}"


class Charter(models.Model):
    class Meta:
        verbose_name = _("Charter")
        verbose_name_plural = _("Charters")

    account = models.ForeignKey("accounts.Account", verbose_name=_("Project account"),on_delete=models.PROTECT)
    scope = models.TextField(verbose_name=_("Project scope")) # description of the project's activities
    start_date = models.DateField(verbose_name=_("Project start date"))
    end_date = models.DateField(verbose_name=_("Project end date"), null=True, blank=True)
    status = models.CharField(Status.choices(), verbose_name=_("Status"), default=Status.ACTIVE)
    secretary_account = models.ForeignKey("accounts.Account", verbose_name=_("Secretary Account"), on_delete=models.PROTECT)

    # these two dates are manual input. They default to today() in the UI only, not in the DB. They may be different from the actual object creation/update date in the database
    creation_date = models.DateField(verbose_name=_("Charter Creation Date"), null=True,blank=True)
    update_date = models.DateField(verbose_name=_("Charter Update Date"), null=True,blank=True)

    # Tokens
    token_initial_value = models.DecimalField(max_digits=10, decimal_places=3, default=10,verbose_name=_("Token initial value"))
    token_indexing_rate = models.DecimalField(max_digits=5, decimal_places=2, default=25,verbose_name=_("Token indexing rate")) # expressed as a percentage per year, eg. 25.53 = 25.53%/yr)

    # Fab→Fahad 2024-10-04: do we need to store it, or can we calculate it on the fly by looking at the revisions
    token_last_revision_value = models.DecimalField(max_digits=10, decimal_places=3, default=10,verbose_name=_("Token last revision value"))
    token_last_revision_date = models.DateField(verbose_name=_("Token last revision date"), null=True,blank=True)

    # This is used from investment contracts, to know if tokens can convert into shares
    can_issue_stock = models.BooleanField(verbose_name=_("Can Issue Stock"), blank=True,null=True)
    stock_type = models.CharField(max_length=255, verbose_name=_("Stock Type"))
    tokens_per_stock = models.DecimalField(max_digits=10, decimal_places=4,verbose_name=_("Tokens Per Stock"))


    def token_value_on(self, on_date: timezone.datetime):
        if on_date >= self.token_last_revision_date:
            return self.token_last_revision_value * (1 + self.token_indexing_rate / 100)**((on_date - self.token_last_revision_date).days / 365.25)
        else:
            latest_revision = TokenRevision.objects.filter(charter=self, date__lt=on_date).order_by('-date').first()
            if not latest_revision:
                raise ValueError("No revision found before the given date")
            return latest_revision.new_value * (1 + latest_revision.new_rate / 100)**((on_date - latest_revision.date).days / 365.25)

    @property
    def current_token_value(self):
        return self.token_value_on(timezone.now())

    # When updating token value or indexing rate, create a new TokenRevision object, link it to this charter, and update the charter's last revision value and indexing rate
    def update_token_value(self, rev_date=timezone.datetime, new_value: Decimal=None, new_rate: Decimal=None, comment: str=None):
        if new_value is None and new_rate is None:
            raise ValueError("At least one of new_value or new_rate must be provided")
        old_value = self.token_value_on(rev_date)
        if new_value is None:
            new_value = old_value
        if new_rate is None:
            new_rate = self.token_indexing_rate
        revision = TokenRevision(charter=self, date=rev_date, old_value=old_value, new_value=new_value, old_rate=self.token_indexing_rate, new_rate=new_rate, comment=comment)
        revision.save()
        self.token_last_revision_value = new_value
        self.token_indexing_rate = new_rate
        self.save()
