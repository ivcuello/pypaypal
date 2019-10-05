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
from pypaypal.errors import PaypalRequestError, PayPalErrorDetail

T = TypeVar('T', bound = 'PayPalEntity')

P = TypeVar('P', bound = 'PaypalPortableAddress')

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
    def __init__(self, json_response: dict= dict(), response_type: ResponseType = ResponseType.MINIMAL):
        self._response_type = response_type
        self._json_response = json_response

    @property
    def json_data(self) -> dict:
        """Getter for this instance private json data
        
        Returns:
            dict -- A deep copy of the instance json attribute
        """
        return copy.deepcopy(self._json_response) if self._json_response else dict()

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
    def __init__(self, errors: bool, api_response, parsed_response: Type[T]=None):
        self.errors = errors
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
    
    @classmethod
    def success(cls, api_response, parsed_response: Type[T] = None) -> 'PaypalApiResponse':
        """Factory method for successful requests
        """
        return cls(False, api_response, parsed_response)
    
    @classmethod
    def error(cls, api_response, parsed_response: Type[T] = None) -> 'PaypalApiResponse':
        """Factory method for unsuccessful requests
        """
        return cls(True, api_response, parsed_response)

class PaypalApiBulkResponse(Generic[Type[T]]):
    """Response wrapper for api responses
    """
    def __init__(self, errors: bool, api_response, parsed_response: List[Type[T]]=None):
        self.errors = errors
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

    @classmethod
    def success(cls, api_response, parsed_response: Type[T] = None) -> 'PaypalApiBulkResponse':
        """Factory method for successful requests
        """
        return cls(False, api_response, parsed_response)
    
    @classmethod
    def error(cls, api_response, parsed_response: Type[T] = None) -> 'PaypalApiBulkResponse':
        """Factory method for unsuccessful requests
        """
        return cls(True, api_response, parsed_response)

class PaypalPage(Generic[Type[T]]):
    """Response wrapper for paged responses
    """
    def __init__(self, error: bool, api_response, total_items: int, total_pages: int, elements: List[T], links: List[ActionLink]):
        self.errors = error
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

    @classmethod
    def success(cls, api_response, total_items: int, total_pages: int, elements: List[T], links: List[ActionLink]) -> 'PaypalPage':
        """Factory method for successful requests
        """
        return cls(False, api_response, total_items, total_pages, elements, links)
    
    @classmethod
    def error(cls, api_response, total_items: int = 0, total_pages: int = 0, elements: List[T] = [], links: List[ActionLink] = []) -> 'PaypalPage':
        """Factory method for unsuccessful requests
        """
        return cls(True, api_response, total_items, total_pages, elements, links)


class Money(PayPalEntity):
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
    
    def __init__(self, seller_transaction_id: str, transaction_status: str, buyer: str, gross_amount: Money, seller: PaypalMerchant, messages: List[PaypalMessage], **kwargs):
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
        gross_amount = Money.serialize_from_json(json_data['dispute_amount'], response_type)
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
        self.address_details = details
        self.postal_code = postal_code
        self.country_code = country_code
        self._admin_areas = { x.adm_number : x.adm_area_info for x in admin_areas }
        self._address_lines = { x.addr_number : x.addr_line_info for x in address_lines }

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
        
    @classmethod
    def serialize_from_json(cls: Type[P], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> P:
        adm_areas, addr_lines, details = [], [], None
        
        for i in range(1, 5):
            prop = 'admin_area_{}'.format(i)
            if prop in json_data.keys():
                adm_areas.append(AdminArea(i, json_data[prop]))

        for i in range(1, 4):
            prop = 'address_line_{}'.format(i)
            if prop in json_data.keys():
                adm_areas.append(AddressLine(i, json_data[prop]))

        j_details = json_data.get('address_details')

        if j_details:
            street = Street(j_details.get('street_number'), j_details.get('street_name'), j_details.get('street_type'))
            details = PaypalAddressDetail(street, j_details.get('delivery_service'), j_details.get('building_name'), j_details.get('sub_building'))

        return cls(json_data.get('country_code'), json_data.get('postal_code'), addr_lines, adm_areas, details)
    
class PatchUpdateRequest:
    def __init__(self, path: str, value: str, operation: str):
        self.path = path
        self.value = value
        self.operation = operation

class PaypalName(PayPalEntity):
    """Name object representation
    """

    def __init__(self, given_name: str, surname: str,  **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.surname = surname
        self.given_name = given_name
        self.prefix = self._json_response.get('prefix', kwargs.get('prefix'))
        self.suffix = self._json_response.get('suffix', kwargs.get('suffix'))
        self.full_name = self._json_response.get('full_name', kwargs.get('full_name'))
        self.middle_name = self._json_response.get('middle_name', kwargs.get('middle_name'))

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['given_name'], json_data['surname'], json_response= json_data, response_type = response_type
        )

class PaypalPhoneDetail(PayPalEntity):
    """Phone detail object representation
    """

    def __init__(self, country_code: str, national_number: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.country_code = country_code
        self.national_number = national_number
        self.phone_type = self._json_response.get('phone_type', kwargs.get('phone_type'))
        self.extension_number = self._json_response.get('extension_number', kwargs.get('extension_number'))

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data.get('country_code'), json_data.get('national_number'), json_response= json_data, response_type = response_type
        )
    
class ContactInformation(PayPalEntity):
    """Contact information object representation
    """
    def __init__(self, business_name: str, name: PaypalName = None, address: PaypalPortableAddress = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.address = address
        self.business_name = business_name

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        address = PaypalPortableAddress.serialize_from_json(json_data)
        name = PaypalName.serialize_from_json(json_data['name']) if 'name' in json_data.keys() else None

        return cls(json_data['business_name'], name, address, json_response= json_data, response_type = response_type)

class BillingInfo(PayPalEntity):
    """Billing info object representation
    """
    def __init__(self, business_name: str, name: PaypalName = None, address: PaypalPortableAddress = None, phones: List[PaypalPhoneDetail] = [], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.phones = phones
        self.address = address
        self.business_name = business_name
        self.language = self._json_response.get('language', kwargs.get('language'))
        self.email_address = self._json_response.get('email_address', kwargs.get('email_address'))
        self.additional_info = self._json_response.get('additional_info', kwargs.get('additional_info'))

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        phones = []
        address = PaypalPortableAddress.serialize_from_json(json_data)
        name = PaypalName.serialize_from_json(json_data['name']) if 'name' in json_data.keys() else None

        j_phones = json_data.get('phones')

        if j_phones:
            phones = [ PaypalPhoneDetail.serialize_from_json(x, response_type) for x in j_phones ]

        return cls(
            json_data['business_name'], name, address, phones, json_response= json_data, response_type = response_type
        )

class RecipientInfo(PayPalEntity):
    """Recipient info object representation
    """
    def __init__(self, billing_info: BillingInfo, shipping_info: ContactInformation, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.billing_info = billing_info
        self.shipping_info = shipping_info
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        billing = BillingInfo.serialize_from_json(json_data['billing_info']) if 'billing_info' in json_data.keys() else None
        shipping = ContactInformation.serialize_from_json(json_data['shipping_info']) if 'shipping_info' in json_data.keys() else None

        return cls(billing, shipping, json_response= json_data, response_type = response_type)

class Tax(PayPalEntity):
    """Tax object representation
    """

    def __init__(self, name: str, percent: str, amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.amount = amount
        self.percent = percent

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount = Money.serialize_from_json(json_data['amount']) if 'amount' in json_data.keys() else None
        return cls(json_data['name'], amount, json_data['pecent'], json_response= json_data, response_type = response_type)

class Discount(PayPalEntity):
    
    def __init__(self, percent: str, amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.amount = amount
        self.percent = percent

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount = Money.serialize_from_json(json_data['amount']) if 'amount' in json_data.keys() else None
        return cls(json_data['pecent'], amount, json_response= json_data, response_type = response_type)

class Item(PayPalEntity):
    """Item object representation
    """

    def __init__(self, id: str, name: str, quantity: str, unit_amount: str, tax: Tax = None, discount: Discount = None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.id = id 
        self.tax = tax
        self.name = name
        self.quantity = quantity 
        self.discount = discount 
        self.unit_amount = unit_amount
        self._item_date = self._json_response.get('item_date', kwargs.get('item_date'))
        self.description = self._json_response.get('description', kwargs.get('description'))
        self.unit_of_measure = self._json_response.get('unit_of_measure', kwargs.get('unit_of_measure'))

    @property
    def item_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._item_date) if self._item_date else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['item_date'] = ret.pop('_item_date', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
                json_data['id'], json_data['name'], json_data['quantity'], json_data['unit_amount'],
                json_response= json_data, response_type = response_type
            )

class AggregatedDiscount(PayPalEntity):
    """Aggregated discount object representation
    """
    def __init__(self, invoice_discount: Discount, item_discount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.item_discount = item_discount
        self.invoice_discount = invoice_discount
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        itm_disc = Discount.serialize_from_json(json_data['item_discount'])
        inv_disc = Discount.serialize_from_json(json_data['invoice_discount'])

        return cls(inv_disc, itm_disc, json_response= json_data, response_type = response_type)

class ShippingCost(PayPalEntity):
    """Shipping Cost object representation
    """
    def __init__(self, tax: Tax, amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.tax = tax
        self.amount = amount

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        tax = Discount.serialize_from_json(json_data['tax'])
        amt = Money.serialize_from_json(json_data['amount'])
        return cls(tax, amt, json_response= json_data, response_type = response_type)

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

class RefundDetail(PayPalEntity):
    """Refund detail object representation
    """

    def __init__(self, rf_type: str, refund_id: str, method: str, refund_date: str, amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.type = rf_type
        self.refund_id = refund_id
        self.method = method
        self.amount = amount        
        self._refund_date = refund_date

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['refund_date'] = ret.pop('_refund_date', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount = Money.serialize_from_json(json_data['amount']) if 'amount' in json_data.keys() else None
        
        return cls(
            json_data['type'], json_data['refund_id'], json_data['method'], json_data['refund_date'], amount,
            json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def for_invoice(cls, refund_date: datetime, amount: Money, method: str) -> T:
        return cls(None, None, method, refund_date.strftime('%Y-%m-%d'), amount)
        
class Refund(PayPalEntity):
    """Refund object representation
    """

    def __init__(self, refund_amount: Money, transactions: List[RefundDetail], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.refund_amount = refund_amount
        self.transactions = transactions

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        refund_amount, transactions = None, list()

        if 'refund_amount' in json_data.keys():
            refund_amount = Money.serialize_from_json(json_data['refund_amount'], response_type)        
        if 'transactions' in json_data.keys():
            transactions = [RefundDetail.serialize_from_json(x, response_type) for x in json_data['transactions']]
        
        return cls(refund_amount, transactions, json_response= json_data, response_type = response_type)

class AmountRange:
    """Amount range for requests
    """
    def __init__(self, lower_amount: Money, upper_amount: Money):
        self.lower_amount = lower_amount
        self.upper_amount = upper_amount
    
    def to_dict(self) -> dict:
        return { 
            'lower_amount': self.lower_amount.to_dict(), 
            'upper_amount': self.upper_amount.to_dict() 
        }

class DateRange:
    """Date range for request
    """
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
    
    def to_dict(self) -> dict:
        return { 'start': self.start, 'end': self.end }

