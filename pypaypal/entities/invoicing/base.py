"""Base module with common entities for invoicing
"""

from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import ( 
    T, 
    Money, 
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
        default_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%s')
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time', default_time))
        self._last_update_time = self._json_response.get('last_update_time', kwargs.get('last_update_time', default_time))

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

    def __init__(self, business_name: str, name: PaypalName = None, address : PaypalPortableAddress = None, phones: List[PaypalPhoneDetail] = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.phones = phones
        self.address = address
        self.business_name = business_name
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
        address, name, phones = None, None, []
        
        if 'name' in json_data.keys():
            name = PaypalName.serialize_from_json(json_data['name'], response_type)
        
        if 'address' in json_data.keys():
            address = PaypalPortableAddress.serialize_from_json(json_data['address'], response_type)

        if 'phones' in json_data.keys():
            phones = [PaypalPhoneDetail.serialize_from_json(x, response_type) for x in json_data['phones']]
        
        return cls(
            json_data.get('business_name'), name, address, phones, json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(
        cls, business_name, *, name: PaypalName = None, 
        address : PaypalPortableAddress = None, phones: List[PaypalPhoneDetail] = None, 
        tax_id: str = None, website: str = None, logo_url: str = None, additional_notes: str = None 
    ):        
        return cls(
            business_name, name, address, phones, 
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
        default_time = datetime.now().strftime('%Y-%m-%dT%H:%M:%s')
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time', default_time))

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