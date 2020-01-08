"""    
    Module with subscription plans related entities
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import ( 
    T, 
    Money, 
    ActionLink, 
    PayPalEntity, 
    ResponseType, 
)

class PlanStatus(Enum):
    # The plan was created. You cannot create subscriptions for a plan in this state.
    CREATED = 1
    # The plan is inactive.
    INACTIVE = 2
    # The plan is active. You can only create subscriptions for a plan in this state.
    ACTIVE = 3

class BillingCycleTenureType(Enum):
    # A trial billing cycle.
    TRIAL = 1
    # A regular billing cycle.
    REGULAR = 2

class FrequencyIntervalUnit(Enum):
    # A daily billing cycle.
    DAY = 1 
    # A weekly billing cycle.
    WEEK = 2
    # A monthly billing cycle.
    MONTH = 3
    # A yearly billing cycle.
    YEAR = 4


class PricingScheme(PayPalEntity):
    """Billing cycle pricing scheme obj representation
    """
    def __init__(self, *, version: int = None, fixed_price: Money = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.version = version
        self.fixed_price = fixed_price
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time'))
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
    
    @property
    def update_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._update_time) if self._update_time else None
        except:
            return None

    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    @classmethod
    def create(cls, *, version: int = None, fixed_price: Money = None) -> 'PricingScheme':
        return cls(version = version, fixed_price = fixed_price)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        args = { **json_data }
        if 'fixed_price' in json_data.keys():
            args['fixed_price'] = Money.serialize_from_json(json_data['fixed_price'])
        return cls(**args, json_response= json_data, response_type = response_type)


class Frequency(PayPalEntity):
    """Billing cycle frequency obj representation
    """

    def __init__(self, )

class BillingCycle(PayPalEntity):
    """Plan billing cycle obj representation.
    """

    def __init__(self, pricing_schemes: )