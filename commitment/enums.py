
# c:/Users/fabri/Repos/flexup/flexup-backend/payment_term/enums.py

from click import group
from enum_properties import EnumProperties
from decimal import Decimal as Dec
from django.utils.translation import gettext_lazy as _

from enum_properties import EnumProperties

class FlexUpEnum(EnumProperties):
    """
    Add some utility methods to the EnumProperties class.
    """
    label: str  # Ensure 'label' is part of the annotations

#     def __new__(cls, value, label, *args):
#         obj = super().__new__(cls, value)
#         obj.label = label
#
#         # Retrieve the annotations of the subclass
#         annotations = cls.__annotations__
#
#         # Ensure the number of args matches the number of annotations
#         if len(args) != len(annotations):
#             raise ValueError(
#                 f"{cls.__name__} expects {len(args)} arguments, got {len(args)}."
#             )
#
#         # Assign each argument to the corresponding annotated attribute
#         for attr, arg in zip(annotations.keys(), args):
#             setattr(obj, attr, arg)
#
#         return obj

    @classmethod
    def choices(cls):
        return [(item.value, item.label) for item in cls]

    @classmethod
    def choices_list(cls, *allowed_values):
        """
        Return a filtered list of choices based on allowed enum values.
        :param allowed_values: Enum values to be included in the choices
        :return: List of tuples (value, label) with allowed choices
        """
        return [(item.value, item.label) for item in cls if item.name in allowed_values]

    @classmethod
    def filter_by(cls, property_name):
        """
        Return a list of choices where the given property is not None.
        :param property_name: The name of the property to filter by.
        :return: List of tuples (value, label) where the property is not None
        """
        return [
            (item.value, item.label)
            for item in cls
            if getattr(item, property_name, None) is not None
        ]


class Period(FlexUpEnum):
    label: str
    duration: float
    periodicity: str
    interest_rf: Dec
    residue_rf: Dec
    short_name: str

    # name     value  label               duration     periodicity      interest_rf    residue_rf    short_name
    YEAR =    'Y',  _('Year'),             365.25,   _('Yearly'),          Dec(0.9),     Dec(1),       _('Y')
    QUARTER = 'Q',  _('Quarter'),          91.3125,  _('Quarterly'),       Dec(0.8),     Dec(0.8),     _('Q')
    MONTH =   'M',  _('Month'),            30.4375,  _('Monthly'),         Dec(0.6),     Dec(0.6),     _('M')
    WEEK =    'W',  _('Week'),             7,        _('Weekly'),          None,         None,         _('W')
    DAY =     'D',  _('Day'),              1,        _('Daily'),           None,         None,         _('S')
    SAME =    'A',  _('Same as primary'),  None,     _('Same as primary'), Dec(1),       Dec(1),       _('Same')
    NA =      'N',  _('Not applicable'),   None,     _('Not applicable'),  Dec(1),       Dec(1),       ''


class Priority(FlexUpEnum):
    label: str
    group: str
    period: Period
    special: bool
    primary_rf: Dec
    interest_rf: Dec
    level: int
    residue_rf: Dec
    short_name: str

    # name       value     label                group        period        special  primary_rf   interest_rf   level  residue_rf   short_name
    FIRM         = 'R',   _('Firm'),            'Base',      Period.MONTH,   None,      0,           0.5,         1,          None,       _('Firm'),
    PREFERRED    = 'P',   _('Preferred'),       'Base',      Period.MONTH,   None,    0.2,           0.6,         2,           0.7,       _('Pref.'),
    FLEX         = 'F',   _('Flex'),            'Flexible',  Period.MONTH,   None,    0.4,           0.7,         3,           0.8,       _('Flex'),
    SUPERFLEX    = 'S',   _('Superflex'),       'Flexible',  Period.MONTH,   None,    0.6,           0.8,         4,           0.9,       _('SupFlx'),
    CREDIT       = 'C',   _('Credit'),          'Equity',    Period.YEAR,    None,    0.8,           0.9,         5,             1,       _('Credit'),
    TOKEN        = 'T',   _('Token'),           'Equity',    Period.YEAR,    None,      1,          None,      None,          None,       _('Token'),
    SAME         = 'A',   _('Same as primary'), 'Special',   None,           True,    None,            1,      None,          None,       _('Same'),
    DISTRIBUTION = 'D',   _('Distribution'),    'Special',   Period.YEAR,    True,    None,         None,      None,          None,       _('Dist.'),
    NA           = 'N',   _('Not applicable'),  'Special',   None,           True,    None,            1,      None,             1,       _('NA')


class StartDate(FlexUpEnum):
    label: str
    primary_rf: Dec
    interest_rf: Dec
    short_name: str

    # name           value   label                   primary_rf  interest_rf  short_name
    CONFIRMATION =    'O',  _('Order confirmation'),  0.7,         0.85,       _('OC')
    DELIVERY_START =  'S',  _('Delivery start'),      0.8,         0.9,        _('DS')
    DELIVERY_MIDDLE = 'M',  _('Delivery middle'),     0.9,         0.95,       _('DM')
    DELIVERY_FINISH = 'F',  _('Delivery finish'),     1,           1,          _('DF')
    DUE_DATE =        'D',  _('Intial due date'),     None,        1,          _('DD')
    NA =              'N',  _('Not applicable'),      1,           1,          _('NA')


class PrimaryAdjustment(FlexUpEnum):
    label: str
    adjustment_factor: Dec
    short_name: str
    # name  value  label                  amount    short_name
    BOP =  'B',    _('Beginning of period'),  -0.5,    _('BOP')
    EOP =  'E',    _('End of period'),         0.5,    _('EOP')
    NONE = 'N', _('No adjustment'),              0,    '',


class TokenRedemption(FlexUpEnum):
    label: str
    redemption_rf: Dec
    short_name: str
    short_name: str

    # name    value    label                       redemption_rf   short_name
    YES =    'Y',     _('Redeemable tokens'),      1.25,             _('Red.')
    NO =     'N',     _('Non-redeemable tokens'),  1,                None