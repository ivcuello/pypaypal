"""Base module with common entities for invoicing
"""

from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import ( 
    T, 
    Tax,
    Money, 
    Discount,
    PaypalName,
    PayPalEntity, 
    ResponseType, 
    PaypalPhoneDetail,
    PaypalPortableAddress
)

class MetaData(PayPalEntity):
    """Template audit metadata.
    """

    def __init__(self, created_by: str, last_updated_by: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.created_by = created_by
        self.last_updated_by = last_updated_by
        # default_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%s')
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
        self._last_update_time = self._json_response.get('last_update_time', kwargs.get('last_update_time'))

    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    @property
    def last_updated_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._last_updated_time) if self._last_updated_time else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['create_time'] = ret.pop('_create_time', None)
        ret['last_updated_time'] = ret.pop('_last_updated_time', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data.get('created_by'), json_data.get('last_updated_by'), json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(cls, created_by: str, last_updated_by: str) -> 'MetaData':
        creation = datetime.now().strftime('%Y-%m-%dT%H:%M:%s')
        
        return cls(
            created_by, last_updated_by, 
            created_time = creation, last_update_time = creation
        )

class InvoicerInfo(PayPalEntity):
    """Invoicer info object representation
    """

    _ARRAY_TYPES = { 'phones': PaypalPhoneDetail }
    _ENTITY_TYPES = {'name': PaypalName, 'address': PaypalPortableAddress }

    def __init__(self, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name: PaypalName = kwargs.get('name')
        self.email_address: str = kwargs.get('email_address')
        self.business_name: str = kwargs.get('business_name')
        self.address : PaypalPortableAddress = kwargs.get('address')
        self.phones: List[PaypalPhoneDetail] = kwargs.get('phones')
        self.tax_id = self._json_response.get('tax_id', kwargs.get('tax_id'))
        self.website = self._json_response.get('website', kwargs.get('website'))
        self.logo_url = self._json_response.get('logo_url', kwargs.get('logo_url'))
        self.additional_notes = self._json_response.get('additional_notes', kwargs.get('additional_notes'))

    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.phones:
            ret['phones'] = [ x.to_dict() for x in self.phones ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES, cls._ARRAY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

    @classmethod
    def create(
        cls, business_name, *, name: PaypalName = None, 
        address : PaypalPortableAddress = None, phones: List[PaypalPhoneDetail] = None, 
        tax_id: str = None, website: str = None, logo_url: str = None, additional_notes: str = None 
    ):        
        return cls(
            business_name=business_name, name=name, address=address, phones=phones, 
            tax_id = tax_id, website = website, logo_url = logo_url,
            additional_notes = additional_notes
        )
    
class PartialPayment(PayPalEntity):
    """Partial payment object representation
    """
    
    def __init__(self, minimum_amount_due: Money, allow_partial_payment: bool, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.minimum_amount_due = minimum_amount_due
        self.allow_partial_payment = allow_partial_payment

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount = Money.serialize_from_json(json_data['minimum_amount_due'])
        return cls(amount, json_data.get('allow_partial_payment'), json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, minimum_amount_due: Money, allow_partial_payment: bool = False):
        return cls(minimum_amount_due, allow_partial_payment)

class FileReference(PayPalEntity):
    """File reference object representation
    """

    def __init__(self, file_id: str, reference_url: str, content_type: str, size: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.id = file_id
        self.reference_url = reference_url
        self.content_type = content_type
        self.size = size
        # default_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))

    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['create_time'] = ret.pop('_create_time', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data.get('id'), json_data.get('reference_url'), json_data.get('content_type'),
            json_data.get('size'), json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(cls, file_id: str, reference_url: str, content_type: str, size: str, creation: datetime = datetime.now()) -> 'FileReference':
        return cls(file_id, reference_url, content_type, size, create_time = creation.strftime('%Y-%m-%dT%H:%M:%s'))

class AggregatedDiscount(PayPalEntity):
    """Aggregated discount object representation
    """

    _ENTITY_TYPES = { 'invoice_discount': Discount, 'item_discount': Money }

    def __init__(self, invoice_discount: Discount = None, item_discount: Money = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.item_discount = item_discount
        self.invoice_discount = invoice_discount
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

class ShippingCost(PayPalEntity):
    """Shipping Cost object representation
    """

    _ENTITY_TYPES = { 'tax': Tax, 'amount': Money }

    def __init__(self, tax: Tax, amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.tax = tax
        self.amount = amount

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

class CustomAmount(PayPalEntity):
    """Custom amount object representation
    """
    def __init__(self, label: str, amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.label = label
        self.amount = amount

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amt = Money.serialize_from_json(json_data['amount'])
        return cls(json_data['label'], amt, json_response= json_data, response_type = response_type)

class AmountWithBreakdown(PayPalEntity):
    """Amount with breakdown object representation
    """

    def __init__(self, item_total: Money, discount: AggregatedDiscount, tax_total: Money, shipping: ShippingCost, custom: CustomAmount, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))        
        self.item_total = item_total
        self.discount = discount
        self.tax_total = tax_total
        self.shipping = shipping
        self.custom = custom

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        item_total, discount, tax_total, shipping, custom = None, None, None, None, None
        
        if 'item_total' in json_data.keys():
            item_total = Money.serialize_from_json(json_data['item_total'])
        if 'discount' in json_data.keys():
            discount = AggregatedDiscount.serialize_from_json(json_data['discount'])
        if 'tax_total' in json_data.keys():
            tax_total = Money.serialize_from_json(json_data['tax_total'])
        if 'shipping' in json_data.keys():
            shipping = ShippingCost.serialize_from_json(json_data['shipping'])
        if 'custom' in json_data.keys():
            custom = CustomAmount.serialize_from_json(json_data['custom'])

        return cls(item_total, discount, tax_total, shipping, custom, json_response= json_data, response_type = response_type)

class AmountSummaryDetail(PayPalEntity):
    """Amount sumary object representation
    """

    # Serializable simple paypal entities
    _ENTITY_TYPES = { 'breakdown': AmountWithBreakdown }

    def __init__(self, currency_code: str = None, value: str = None, breakdown: AmountWithBreakdown = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.value = value
        self.currency_code = currency_code
        self.breakdown = breakdown

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)
            
    @classmethod
    def create(cls, currency_code: str, value: str, breakdown: AmountWithBreakdown) -> 'AmountSummaryDetail':
        return cls(currency_code, value, breakdown)
