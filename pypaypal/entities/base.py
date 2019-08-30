"""
    Module with serialized object representations of paypal responses
"""
import copy
from enum import Enum
from datetime import datetime

from abc import ABC, abstractmethod
from email.mime.base import MIMEBase
from typing import Type, TypeVar, List, Generic


import dateutil.parser

from pypaypal.http import PayPalSession
from pypaypal.errors import EntityRefreshError, PaypalRequestError, PayPalErrorDetail

T = TypeVar('T', bound = 'PayPalEntity')

class ResponseType(Enum):
    MINIMAL = 1
    REPRESENTATION = 2

    def is_minimal(self) -> bool:
        """checks if this response type is minimal
        
        Returns:
            bool -- True if MINIMAL False otherwise
        """
        return self == ResponseType.MINIMAL

    def as_header_value(self) -> str:
        """Gets the header value for this return type. E.g: Prefer: return={type} 
        
        Returns:
            str -- the header value
        """
        return 'return=representation' if self == ResponseType.REPRESENTATION else 'return=minimal'

class RequestMethod(Enum):
    """Enumeration for request methods    
    """
    GET = 1
    POST = 2
    PUT = 3
    DELETE = 4
    PATCH = 5

class PayPalEntity(ABC):
    """
        Base class with common properties for serialized paypal entities
    """
    def __init__(self, json_response: dict= None, response_type: ResponseType = ResponseType.MINIMAL):
        self._response_type = response_type
        self._json_response = json_response

    @property
    def json_data(self) -> dict:
        """Getter for this instance private json data
        
        Returns:
            dict -- A deep copy of the instance json attribute
        """
        return copy.deepcopy(self._json_response) if self._json_response else None

    def to_dict(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        pp_entity_props = { k : v.to_dict() for k,v in d.items() if isinstance(v, PayPalEntity) }
        return { **d, **pp_entity_props }

    @classmethod
    @abstractmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        """Serializes a json to a subclass instance
        
        Arguments:
            cls {Type[T]} -- the class
            json_data {dict} -- the json to serialize
            response_type -- flag with the response type defaults to Minimal
        
        Returns:
            T -- new subsclass instance from json
        """
        pass

class ActionLink(PayPalEntity):
    """Wraping class for entities HATEOAS action links 
    """

    def __init__(self, href: str, rel: str, method: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.rel = rel
        self.href = href
        self._method = method

    @property
    def method(self) -> RequestMethod:
        """Getter for the request method
        
        Returns:
            RequestMethod -- Enumerated constant for the instance request method
        """
        return RequestMethod[self._method]

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        """Serializes a json to a subclass instance
        
        Arguments:
            cls {Type[T]} -- the class
            json_data {dict} -- the json to serialize
            response_type -- flag with the response type defaults to Minimal
        
        Returns:
            T -- new subsclass instance from json
        """
        return cls(json_data['href'], json_data['rel'], json_data['method'], json_data = json_data, response_type = response_type)

class PaypalApiResponse(Generic[Type[T]]):
    """Response wrapper for api responses
    """
    def __init__(self, error: bool, api_response, parsed_response: Type[T]=None):
        self.error = error
        self._raw_response = api_response
        self.parsed_response = parsed_response
    
    @property
    def error_detail(self) -> PayPalErrorDetail:
        """Returns the error details if there was an error in the response
        
        Returns:
            PayPalErrorDetail -- Error details if exists else None
        """
        data = self._raw_response.json()
        return PayPalErrorDetail.serialize_from_json(data) if self.error and data else None

class PaypalApiBulkResponse(Generic[Type[T]]):
    """Response wrapper for api responses
    """
    def __init__(self, error: bool, api_response, parsed_response: List[Type[T]]=None):
        self.error = error
        self._raw_response = api_response
        self.parsed_response = parsed_response
    
    @property
    def error_detail(self) -> PayPalErrorDetail:
        """Returns the error details if there was an error in the response
        
        Returns:
            PayPalErrorDetail -- Error details if exists else None
        """
        data = self._raw_response.json()
        return PayPalErrorDetail.serialize_from_json(data) if self.error and data else None

class PaypalPage(Generic[Type[T]]):
    """Response wrapper for paged responses
    """
    def __init__(self, error: bool, api_response, total_items: int, total_pages: int, elements: List[T], links: List[ActionLink]):
        self.error = error
        self.links = links
        self.elements = elements
        self.total_items = total_items
        self.total_pages = total_pages
        self._raw_response = api_response

    @property
    def error_detail(self) -> PayPalErrorDetail:
        """Returns the error details if there was an error in the response
        
        Returns:
            PayPalErrorDetail -- Error details if exists else None
        """
        data = self._raw_response.json()
        return PayPalErrorDetail.serialize_from_json(data) if self.error and data else None

    @property
    def next_page_link(self) -> ActionLink:
        """Retrieves a link to read the next page.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'next', self.links), None)
        
    @property
    def last_page_link(self) -> ActionLink:
        """Retrieves a link to read the last page.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'last', self.links), None)

    @property
    def first_page_link(self) -> ActionLink:
        """Retrieves a link to read the last page.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'first', self.links), None)

class PaypalAmount(PayPalEntity):
    """Amount object definition for paypal request/responses
    """

    def __init__(self, currency_code: str, value: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.value = value
        self.currency_code = currency_code

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data['currency_code'], json_data['value'], json_response= json_data, response_type = response_type)

class PaypalMerchant(PayPalEntity):
    """Merchant object representation
    """
    
    def __init__(self, email: str, merchant_id: str, name: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.email = email
        self.merchant_id = merchant_id

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['email'], json_data['merchant_id'], json_data['name'],
            json_response= json_data, response_type = response_type
        )

class PaypalMessage(PayPalEntity):
    """Message object representation
    """
    
    def __init__(self, posted_by: str, time_posted: str, content: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.content = content
        self.posted_by = posted_by
        self._time_posted = time_posted
    
    @property
    def time_posted(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['posted_by'], json_data['time_posted'], json_data['content'],
            json_response= json_data, response_type = response_type
        )

class PaypalTransaction(PayPalEntity):
    """Transaction object representation
    """
    
    def __init__(self, seller_transaction_id: str, transaction_status: str, buyer: str, gross_amount: PaypalAmount, seller: PaypalMerchant, messages: List[PaypalMessage], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.buyer = buyer
        self.seller = seller
        self.messages = messages
        self.gross_amount = gross_amount
        self.transaction_status = transaction_status
        self.seller_transaction_id = seller_transaction_id
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time'))
    
    @property
    def create_time(self) -> datetime:
        try:
            return dateutil.parser.parse(self._create_time) if self._create_time else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        seller = PaypalMerchant.serialize_from_json(json_data['seller'], response_type)    
        gross_amount = PaypalAmount.serialize_from_json(json_data['dispute_amount'], response_type)
        messages = [PaypalMessage.serialize_from_json(x, response_type) for x in json_data['messages']]
        
        return cls(
            json_data['seller_transaction_id'], json_data['transaction_status'], 
            json_data['buyer'], gross_amount, seller, messages,
            json_response= json_data, response_type = response_type
        )

class AddressLine:
    """Address line wrapper
    """
    def __init__(self, address_line_number: int, address_line_info: str):
        self.addr_number = address_line_number
        self.addr_line_info = address_line_info

class AdminArea:
    """Address line wrapper
    """
    def __init__(self, admin_area_number: int, admin_area_info: str):
        self.adm_number = admin_area_number
        self.adm_area_info = admin_area_info

class Street:
    """Street definition
    """
    def __init__(self, street_no: str, street_name: str, street_type: str):
        self.street_no = street_no
        self.street_name = street_name
        self.street_type = street_type

class PaypalAddressDetail:
    """Non-portable additional address details 
    """
    def __init__(self, street: Street, delivery_service: str, building_name: str, sub_building: str):
        self._street = street
        self.sub_building = sub_building
        self.building_name = building_name 
        self.delivery_service = delivery_service
    
    @property
    def street_number(self) -> str:
        return self._street.street_no if self._street else None

    @property
    def street_name(self) -> str:
        return self._street.street_name if self._street else None

    @property
    def street_type(self) -> str:
        return self._street.street_type if self._street else None

class PaypalPortableAddress:
    """Paypal portable Addresses object representation
    """
    def __init__(self, country_code: str, postal_code: str, address_lines: List[AddressLine], admin_areas: List[AdminArea], details: PaypalAddressDetail):
        self.postal_code = postal_code
        self.country_code = country_code
        self._admin_areas = { x.adm_index : x.adm_area_info for x in admin_areas }
        self._address_lines = { x.addr_index : x.addr_line_info for x in address_lines }
        self.address_details = details

    def _adm_area_for_index(self, index: int) -> str:
        return self._admin_areas[index].adm_area_info if index in self._admin_areas.keys() else None

    def _address_line_for_index(self, index: int) -> str:
        return self._address_lines[index].addr_line_info if index in self._address_lines.keys() else None

    @property
    def address_line_1(self) -> str:
        return self._address_line_for_index(1)

    @property
    def address_line_2(self) -> str:
        return self._address_line_for_index(2)

    @property
    def address_line_3(self) -> str:
        return self._address_line_for_index(3)

    @property
    def admin_area_1(self) -> str:
        return self._adm_area_for_index(1)

    @property
    def admin_area_2(self) -> str:
        return self._adm_area_for_index(2)

    @property
    def admin_area_3(self) -> str:
        return self._adm_area_for_index(3)
    
    @property
    def admin_area_4(self) -> str:
        return self._adm_area_for_index(4)

    def to_dict(self) -> dict:
        exclude = {'_admin_areas', '_address_lines', 'address_details'}
        d = { k:v for k,v in copy.deepcopy(self.__dict__).items() if not k in exclude }
        d['admin_area_1'] = self.admin_area_1
        d['admin_area_2'] = self.admin_area_2
        d['admin_area_3'] = self.admin_area_3
        d['admin_area_4'] = self.admin_area_4
        d['address_line_1'] = self.address_line_1
        d['address_line_2'] = self.address_line_2
        d['address_line_3'] = self.address_line_3

        return d
        

class PatchUpdateRequest:
    def __init__(self, path: str, value: str, operation: str):
        self.path = path
        self.value = value
        self.operation = operation

# class BillingAgreement(PayPalEntity):
#     pass

# class BillingPlan(PayPalEntity):
#     pass

# class CatalogProduct(PayPalEntity):
#     pass

# class Dispute(PayPalEntity):
#     pass

# class Customer(PayPalEntity):
#     pass

# class Invoice(PayPalEntity):
#     pass

# class Order(PayPalEntity):
#     pass

# class PartnerReferral(PayPalEntity):
#     pass

# class PaymentExpirience(PayPalEntity):
#     pass

# class Payment(PayPalEntity):
#     pass

# class Authorization(PayPalEntity):
#     pass

# class Capture(PayPalEntity):
#     pass

# class Payout(PayPalEntity):
#     pass

# class PayPalSync(PayPalEntity):
#     pass

# class ReferencedPayout(PayPalEntity):
#     pass

# class Subscription(PayPalEntity):
#     pass

# class Vault(PayPalEntity):
#     pass

