
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
    def all_choices(cls):
        return [(item.value, item.label) for item in cls]

    @classmethod
    def filtered_choices(cls, *allowed_values):
        """
        Return a filtered list of choices based on allowed enum values.
        :param allowed_values: Enum values to be included in the choices
        :return: List of tuples (value, label) with allowed choices
        """
        return [(item.value, item.label) for item in cls if item.name in allowed_values]

    @classmethod
    def choices_with_property(cls, property_name):
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
    duration: Dec
    periodicity: str
    interest_rf: Dec
    residue_rf: Dec
    short_name: str

    # name     value  label               duration        periodicity           interest_rf   residue_rf    short_name
    YEAR =    'Y',  _('Year'),             Dec(365.25),   _('Yearly'),          Dec(0.9),     Dec(1),       _('Y')
    QUARTER = 'Q',  _('Quarter'),          Dec(91.3125),  _('Quarterly'),       Dec(0.8),     Dec(0.8),     _('Q')
    MONTH =   'M',  _('Month'),            Dec(30.4375),  _('Monthly'),         Dec(0.6),     Dec(0.6),     _('M')
    WEEK =    'W',  _('Week'),             Dec(7),        _('Weekly'),          None,         None,         _('W')
    DAY =     'D',  _('Day'),              Dec(1),        _('Daily'),           None,         None,         _('S')
    SAME =    'A',  _('Same as primary'),  None,          _('Same as primary'), Dec(1),       Dec(1),       _('Same')
    NA =      'N',  _('Not applicable'),   None,          _('Not applicable'),  Dec(1),       Dec(1),       ''

class Priority(FlexUpEnum):
    label: str
    period: Period
    special: bool
    primary_rf: Dec
    interest_rf: Dec
    interest_level: int
    residue_rf: Dec
    short_name: str

    # name       value     label                period          special  primary_rf   interest_rf interest_level  residue_rf   short_name
    FIRM         = 'R',   _('Firm'),            Period.MONTH,   None,    Dec(0),      Dec(0.5),    1,              None,       _('Firm'),
    PREFERRED    = 'P',   _('Preferred'),       Period.MONTH,   None,    Dec(0.2),    Dec(0.6),    2,              Dec(0.7),   _('Pref.'),
    FLEX         = 'F',   _('Flex'),            Period.MONTH,   None,    Dec(0.4),    Dec(0.7),    3,              Dec(0.8),   _('Flex'),
    SUPERFLEX    = 'S',   _('Superflex'),       Period.MONTH,   None,    Dec(0.6),    Dec(0.8),    4,              Dec(0.9),   _('SupFlx'),
    CREDIT       = 'C',   _('Credit'),          Period.YEAR,    None,    Dec(0.8),    Dec(0.9),    5,              Dec(1),     _('Credit'),
    TOKEN        = 'T',   _('Token'),           Period.YEAR,    None,    Dec(1),      Dec(1),      None,           None,       _('Token'),
    SAME         = 'A',   _('Same as primary'), None,           True,    None,        Dec(1),      None,           None,       _('Same'),
    DISTRIBUTION = 'D',   _('Distribution'),    Period.YEAR,    True,    None,        None,        None,           None,       _('Dist.'),
    NA           = 'N',   _('Not applicable'),  None,           True,    None,        Dec(1),      None,           Dec(1),     _('NA')


class StartDate(FlexUpEnum):
    label: str
    primary_rf: Dec
    interest_rf: Dec
    short_name: str

    # name           value   label                         primary_rf  interest_rf  short_name
    CONFIRMATION =    'O',  _('Order confirmation date'),  Dec('0.7'),  Dec('0.85'),  _('OC')
    DELIVERY_START =  'S',  _('Delivery start date'),      Dec('0.8'),  Dec('0.9'),   _('DS')
    DELIVERY_MIDDLE = 'M',  _('Delivery middle date'),     Dec('0.9'),  Dec('0.95'),  _('DM')
    DELIVERY_FINISH = 'F',  _('Delivery finish date'),     Dec('1'),    Dec('1'),     _('DF')
    DUE_DATE =        'D',  _('Intial due date'),          None,        Dec('1'),     _('DD')
    NA =              'N',  _('Not applicable'),           Dec('1'),    Dec('1'),     _('NA')

class PrimaryAdjustment(FlexUpEnum):
    label: str
    adjustment_factor: Dec
    short_name: str

    BOP =  'B', 'Beginning of period',  Dec('-0.5'),    _('BOP')
    EOP =  'E', 'End of period',        Dec('0.5'),     _('EOP')
    NONE = 'N', 'No adjustment',        Dec('0'),       ''

class TokenRedemption(FlexUpEnum):
    label: str
    redemption_rf: Dec
    short_name: str
    short_name: str

    # name    value    label                       redemption_rf   short_name
    YES =    'Y',     _('Redeemable tokens'),      Dec('1.25'),      _('Red.')
    NO =     'N',     _('Non-redeemable tokens'),  Dec('1'),         None