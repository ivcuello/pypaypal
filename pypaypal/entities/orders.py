"""
    Module with all Order related entities.
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import ( 
    T, 
    Money,
    PaypalName,
    ActionLink,
    ResponseType,
    PayPalEntity,
    PaypalPhoneDetail,
    PaypalPortableAddress
)

class PhoneType(Enum):
    FAX = 1
    HOME = 2
    MOBILE = 3
    OTHER = 4
    PAGER = 5

class OrderIntent(Enum):
    CAPTURE = 1
    AUTHORIZE = 2

class TaxIdType(Enum):
    BR_CPF = 1 # Individual tax id type
    BR_CNPJ = 2 # Business tax id type

class DisbursementMode(Enum):
    INSTANT = 1
    DELAYED = 2

class ItemCategory(Enum):
    DIGITAL_GOODS = 1
    PHYSICAL_GOODS = 2

class LandingPage(Enum):
    LOGIN = 1
    BILLING = 2
    NO_PREFERENCE = 3

class ShippingPreference(Enum):
    GET_FROM_FILE = 1
    NO_SHIPPING = 2
    SET_PROVIDED_ADDRESS = 3

class UserAction(Enum):
    CONTINUE = 1
    PAY_NOW = 2

class PayeePreference(Enum):
    UNRESTRICTED = 1
    IMMEDIATE_PAYMENT_REQUIRED = 2

class OrderStatus(Enum):
    CREATED = 1
    SAVED = 2
    APPROVED = 3
    VOIDED = 4
    COMPLETED = 5

class CardType(Enum):    
    VISA = 1 # Visa card.
    MASTERCARD = 2  # MasterCard card.
    DISCOVER = 3 # Discover card.
    AMEX = 4 # American Express card.
    SOLO = 5 # Solo debit card.
    JCB = 6 # Japan Credit Bureau card.
    STAR = 7 # Military Star card.
    DELTA = 8 # Delta Airlines card.
    SWITCH = 9 # Switch credit card.
    MAESTRO = 10 # Maestro credit card.
    CB_NATIONALE = 11 # Carte Bancaire (CB) credit card.
    CONFIGOGA = 12 # Configoga credit card.
    CONFIDIS = 13 # Confidis credit card.
    ELECTRON = 14 # Visa Electron credit card.
    CETELEM = 15 # Cetelem credit card.
    CHINA_UNION_PAY = 16 # China union pay credit card.

class TokenType(Enum):
    BILLING_AGREEMENT = 1 # Approved recurring payment for goods or services.


class TypedPhone(PayPalEntity):
    """Paypal Phone with type object representation.
    """
    def __init__(self, phone_type: str, phone_number: PaypalPhoneDetail, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.phone_type = phone_type
        self.phone_number = phone_number
    
    def to_dict(self) -> dict:
        d = super().to_dict()
        d['phone_number'] = { 'national_number': self.phone_number.national_number }
        return d

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        phone_number = None

        if 'phone_number' in json_data.keys():
            phone_number = PaypalPhoneDetail.serialize_from_json(json_data['phone_number'], response_type)
        
        return cls(
            json_data['phone_type'], phone_number, json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(cls, phone_type: PhoneType, phone_number: PaypalPhoneDetail) -> 'TypedPhone':
        return cls(phone_type, phone_number)

class TaxInfo(PayPalEntity):
    """Payer tax info object representation
    """
    def __init__(self, tax_id: str, tax_id_type: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.tax_id = tax_id
        self.tax_id_type = tax_id_type
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['tax_id'], json_data['tax_id_type'], json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(cls, tax_id: str, tax_id_type: TaxIdType) -> 'TaxInfo':
        return cls(tax_id, tax_id_type.name)

class Payer(PayPalEntity):
    """Paypal Payer object representation
    """
    def __init__(
        self, payer_id: str, name: PaypalName, email_addr: str, 
        phone: TypedPhone, birth_date: str, tax_info: TaxInfo, 
        address: PaypalPortableAddress, **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))    
        self.payer_id = payer_id
        self.name = name
        self.email_address = email_addr 
        self.phone = phone
        self._birth_date = birth_date
        self.tax_info = tax_info 
        self.address = address

    def to_dict(self) -> dict:
        d = super().to_dict()
        if['_birth_date'] in d.keys():
            d['birth_date'] = d.pop('_birth_date')
        return d

    @property
    def birth_date(self) -> datetime:
        try:
            return datetime.strptime(self._birth_date, '%Y-%m-%d') if self._birth_date != None else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        name, phone, tax_info, address = None, None, None, None

        if 'name' in json_data.keys():
            name = PaypalName.serialize_from_json(json_data['name'], response_type)
        if 'phone' in json_data.keys():
            phone = TypedPhone.serialize_from_json(json_data['phone'], response_type)
        if 'tax_info' in json_data.keys():
            tax_info = TaxInfo.serialize_from_json(json_data['tax_info'], response_type)
        if 'address' in json_data.keys():
            address = PaypalPortableAddress.serialize_from_json(json_data['address'], response_type)

        return cls(
            json_data['payer_id'], name, json_data['email_address'], phone, 
            json_data.get('birth_date'), tax_info, address, json_response= json_data, 
            response_type = response_type
        )

    @classmethod
    def create(
        cls, payer_id: str, name: PaypalName = None, email_addr: str = None,
        phone: TypedPhone = None, birth_date: str = None, tax_info: TaxInfo  = None, 
        address: PaypalPortableAddress = None
    ) -> 'Payer':
        return cls(payer_id, name, email_addr, phone, birth_date, tax_info, address)

class AmountBreakdown(PayPalEntity):
    """Amount breakdown detail
    """
    def __init__(
        self, item_total: Money, shipping: Money, handling: Money, 
        tax_total: Money, insurance: Money, shipping_discount: Money,
        discount: Money, **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))    
        self.item_total = item_total
        self.shipping = shipping
        self.handling  = handling 
        self.tax_total = tax_total
        self.insurance = insurance
        self.shipping_discount = shipping_discount
        self.discount = discount
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        breakdown = { 
            'item_total': None, 'shipping': None, 'handling': None, 
            'tax_total': None, 'insurance': None, 'shipping_discount': None, 
            'discount': None
        }

        breakdown = { k : Money.serialize_from_json(json_data[k], response_type) if k in json_data.keys() else None for k in breakdown }

        return cls(**breakdown, json_response = json_data, response_type = response_type)
    
    @classmethod
    def create(cls, *, item_total: Money = None, shipping: Money = None, handling: Money = None, 
        tax_total: Money = None, insurance: Money = None, shipping_discount: Money = None,
        discount: Money = None):
        return cls(item_total, shipping, handling, tax_total, insurance, shipping_discount, discount)

class AmountWithBreakdown(PayPalEntity):
    """Amount with breakdown object representations for order entities
    """
    def __init__(self, currency_code: str, value: str, breakdown: AmountBreakdown, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.currency_code = currency_code
        self.value = value
        self.breakdown = breakdown
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        breakdown = AmountBreakdown.serialize_from_json(json_data['breakdown'], response_type) if 'breakdown' in json_data.keys() else None
        return cls(
            json_data.get('currency_code'), json_data.get('value'), breakdown,
            json_response = json_data, response_type = response_type
        )
    
    @classmethod
    def create(cls, currency_code: str, value: str, breakdown: AmountWithBreakdown = None):
        return cls(currency_code, value, breakdown)

class PayeeBase(PayPalEntity):
    """Payee base object representation.
    """
    def __init__(self, email: str, merchant_id: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.email_address = email
        self.merchant_id = merchant_id

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['email_address'], json_data['merchant_id'],
            json_response= json_data, response_type = response_type
        )

class Payee(PayeeBase):
    """Payee object representation.
    """
    def __init__(self, email: str, merchant_id: str, **kwargs):
        super().__init__(email, merchant_id, **kwargs)

class PlatformFee(PayPalEntity):
    """Platform Fee object representation.
    """
    def __init__(self, amount: Money, payee: PayeeBase, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.payee = payee
        self.amount = amount
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount, payee = None, None

        if 'amount' in json_data.keys():
            amount = Money.serialize_from_json(json_data['amount'], response_type)
        if 'payee' in json_data.keys():
            payee = PayeeBase.serialize_from_json(json_data['payee'], response_type)

        return cls(amount, payee, json_response= json_data, response_type = response_type)

class PaymentInstruction(PayPalEntity):
    """Payment instruction object representation.
    """

    def __init__(self, platform_fees: List[PlatformFee], disbursement_mode: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.platform_fees = platform_fees
        self.disbursement_mode = disbursement_mode

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        platform_fees = []

        if 'platform_fees' in json_data.keys():
            platform_fees = [PlatformFee.serialize_from_json(x, response_type) for x in json_data['platform_fees']]

        return cls(platform_fees, json_data['disbursement_mode'], json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, platform_fees: List[PlatformFee], disbursement_mode: DisbursementMode = DisbursementMode.INSTANT):
        return cls(platform_fees, disbursement_mode.name)

class Item(PayPalEntity):
    """Order item obj representation. Yes... it's different from the Item class in the base module
    """
    def __init__(
        self, name: str, unit_amount: Money, tax: Money, quantity: str, 
        category: str, description: str = None, sku: str = None, **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.unit_amount = unit_amount
        self.tax = tax
        self.quantity = quantity
        self.category = category
        self.description = description
        self.sku = sku

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        unit_amount, tax = None, None

        if 'unit_amount' in json_data.keys():
            unit_amount = Money.serialize_from_json(json_data['unit_amount'], response_type)
            
        if 'tax' in json_data.keys():
            tax = Money.serialize_from_json(json_data['tax'], response_type)
        
        return cls(
            json_data.get('name'), unit_amount, tax, json_data.get('quantity'),
            json_data.get('category'), json_data.get('description'), json_data.get('sku'),
            json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(
        cls, name: str, unit_amount: Money, tax: Money, quantity: int, 
        category: ItemCategory, *, description: str = None, sku: str = None
    ):
        return cls(name, unit_amount, tax, quantity, category.name, description, sku)

class Name(PayPalEntity):
    """Order name obj representation.
    """
    def __init__(self, full_name: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.full_name = full_name

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data['full_name'], json_response= json_data, response_type = response_type)

class ShippingDetail(PayPalEntity):
    """Shipping detail obj representation
    """

    def __init__(self, name: Name, address: PaypalPortableAddress, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.address = address
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        name, address = None, None

        if 'name' in json_data.keys():
            name = Name.serialize_from_json(json_data['name'], response_type)
        if 'address' in json_data.keys():
            address = PaypalPortableAddress.serialize_from_json(json_data['address'], response_type)
        
        return cls(name, address, json_response= json_data, response_type = response_type)
    
    @classmethod
    def create(cls, full_name: str, address: PaypalPortableAddress) -> 'ShippingDetail':
        return cls(Name(full_name), address)

class PurchaseUnitRequest(PayPalEntity):
    """Purchase unit object representation.
    """
    def __init__(
        self, reference_id: str, amount: AmountWithBreakdown, payee: Payee, 
        payment_instruction: PaymentInstruction, description: str, custom_id: str,
        invoice_id: str, pur_id: str, soft_descriptor: str, items: List[Item], 
        shipping: ShippingDetail, **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.reference_id = reference_id
        self.amount = amount
        self.payee  = payee
        self.payment_instruction = payment_instruction
        self.description = description
        self.custom_id = custom_id
        self.invoice_id = invoice_id
        self.id = pur_id
        self.soft_descriptor = soft_descriptor
        self.items  = items
        self.shipping = shipping

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        payee, amount, payment_instruction, shipping, items = None, None, None, None, []
        
        if 'payee' in json_data.keys():
            payee = Payee.serialize_from_json(json_data['payee'], response_type)
        if 'amount' in json_data.keys():
            amount = AmountWithBreakdown.serialize_from_json(json_data['amount'], response_type)
        if 'payment_instruction' in json_data.keys():
            payment_instruction = PaymentInstruction.serialize_from_json(json_data['payment_instruction'], response_type)
        if 'shipping' in json_data.keys():
            shipping = ShippingDetail.serialize_from_json(json_data['shipping'], response_type)

        return cls(
            json_data.get('reference_id'), amount, payee, payment_instruction, json_data.get('description'), 
            json_data.get('custom_id'), json_data.get('invoice_id'), json_data.get('pur_id'), json_data.get('soft_descriptor'), 
            items, shipping, json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(
        cls, amount: AmountWithBreakdown, *, reference_id: str = None, payee: Payee = None,
        payment_instruction: PaymentInstruction = None, description: str = None, custom_id: str = None,
        invoice_id: str = None, pur_id: str = None, soft_descriptor: str = None, items: List[Item] = [],
        shipping: ShippingDetail = None
    ):
        return cls(
            amount, reference_id, payee, payment_instruction, description, custom_id, 
            invoice_id, pur_id, soft_descriptor, items, shipping
        )

class PaymentMethod(PayPalEntity):
    """Order payment method obj representation
    """

    def __init__(self, payer_selected: str, payee_preferred: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.payer_selected = payer_selected
        self.payee_preferred = payee_preferred

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data['payer_selected'], json_data['payee_preferred'], json_response= json_data, response_type = response_type)
    
    @classmethod
    def create(cls,  payee_preferred: PayeePreference, payer_selected: str = 'PAYPAL') -> 'PaymentMethod':
        return cls(payer_selected, payee_preferred.name)

class OrderApplicationContext(PayPalEntity):
    """Paypal Order object representation
    """

    def __init__(
        self, brand_name: str, locale: str, landing_page: str,
        shipping_preference: str, user_action: str, 
        payment_method: PaymentMethod, return_url: str, 
        cancel_url: str, **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.brand_name = brand_name
        self.locale = locale
        self.landing_page = landing_page
        self.shipping_preference = shipping_preference
        self.user_action = user_action
        self.payment_method = payment_method
        self.return_url  = return_url
        self.cancel_url = cancel_url
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        payment_method = None

        if 'payment_method' in json_data.keys():
            payment_method = PaymentMethod.serialize_from_json(json_data['payment_method'], response_type)
        
        return cls(
            json_data.get('brand_name'), json_data.get('locale'), json_data.get('landing_page'), 
            json_data.get('shipping_preference'), json_data.get('user_action'), payment_method, 
            json_data.get('return_url'), json_data.get('cancel_url'),
            json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(cls, brand_name: str, locale: str, return_url: str, cancel_url: str, 
        payment_method: PaymentMethod, landing_page: LandingPage = LandingPage.NO_PREFERENCE,
        shipping_preference: ShippingPreference = ShippingPreference.GET_FROM_FILE, 
        user_action: UserAction = UserAction.CONTINUE ) -> 'OrderApplicationContext':
        return cls(
            brand_name, locale, landing_page.name, shipping_preference.name, 
            user_action.name, payment_method, return_url, cancel_url
        )

class Order(PayPalEntity):
    """Paypal Order object representation
    """

    def __init__(self, intent: str, payer: Payer, purchase_units: List[PurchaseUnitRequest], application_context: OrderApplicationContext, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.intent = intent
        self.payer = payer
        self.purchase_units = purchase_units
        self.application_context = application_context
        self.status = self._json_response.get('status')
        self._create_time = self._json_response.get('create_time')
        self._update_time = self._json_response.get('update_time')
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @property
    def status_enum(self) -> OrderStatus:
        """Status of the order as an enum constant
        
        Returns:
            OrderStatus -- An enumerated constant representing the order status or None
        """
        try:
            return OrderStatus[self.status] if self.status else None
        except:
            return None

    @property
    def create_time(self) -> datetime:
        try:
            return datetime.strptime(self._create_time, '%Y-%m-%d') if self._create_time != None else None
        except:
            return None

    @property
    def update_time(self) -> datetime:
        try:
            return datetime.strptime(self._update_time, '%Y-%m-%d') if self._update_time != None else None
        except:
            return None

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @property
    def approve_link(self) -> ActionLink:
        """Retrieves a link to make an approval on this order.
        
        Returns:
            ActionLink -- The link for the API action.
        """
        return next(filter(lambda x: x.rel == 'approve', self.links), None)

    @property
    def capture_link(self) -> ActionLink:
        """Retrieves a link to capture a payment for this order.
        
        Returns:
            ActionLink -- The link for the API action.
        """
        return next(filter(lambda x: x.rel == 'capture', self.links), None)

    def to_dict(self) -> dict:
        d = super().to_dict()
        if['_birth_date'] in d.keys():
            d['birth_date'] = d.pop('_birth_date')
        return d

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        payer, application_context, purchase_units = None, None, []

        if 'payer' in json_data.keys():
            payer = Payer.serialize_from_json(json_data['payer'], response_type)
        if 'application_context' in json_data.keys():
            application_context = OrderApplicationContext.serialize_from_json(json_data['application_context'], response_type)
        
        if 'purchase_units' in json_data.keys():
            purchase_units = [PurchaseUnitRequest.serialize_from_json(x, response_type) for x in json_data['purchase_units']]

        return cls(json_data.get('intent'), payer, purchase_units, application_context, json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, intent: OrderIntent, payer: Payer, purchase_units: List[PurchaseUnitRequest], application_context: OrderApplicationContext = None) -> 'Order':
        return cls(intent, payer, purchase_units, application_context)

class Card(PayPalEntity):
    """PaymentSource.card object representation.
    """
    def __init__(
        self, card_id: str, name: str, number: str, expiry: str, 
        security_code: str, last_digits: str, card_type: str, 
        billing_address: PaypalPortableAddress, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.name = name
        self.id = card_id
        self.number = number
        self.expiry = expiry
        self.security_code = security_code
        self.last_digits = last_digits
        self.card_type = card_type
        self.billing_address = billing_address

    @property
    def card_type_enum(self) -> OrderStatus:
        """Status of the order as an enum constant
        
        Returns:
            OrderStatus -- An enumerated constant representing the order status or None
        """
        try:
            return CardType[self.card_type] if self.card_type else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        billing_address = None

        if 'billing_address' in json_data.keys():
            billing_address = PaypalPortableAddress.serialize_from_json(json_data['billing_address'], response_type)
        
        return cls(
            json_data.get('id'), json_data.get('name'), json_data.get('number'),
            json_data.get('expiry'), json_data.get('security_code'), json_data.get('last_digits'),
            json_data.get('card_type'), billing_address, json_response= json_data,
            response_type = response_type
        )

    @classmethod
    def create(
        cls, number: str, expiry: str, *, name: str = None, 
        security_code: str = None, billing_address: PaypalPortableAddress = None) -> 'Card':
        # CardType will remain as "str" to keep flexibilty in case there's another supported network.
        return cls(None, name, number, expiry, security_code, None, None, billing_address)

class Token(PayPalEntity):
    """PaymentSource.token object representation.
    """
    def __init__(self, token_id: str, token_type: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.id = token_id
        self.type= token_type

    @property
    def token_type_enum(self) -> OrderStatus:
        """Status of the order as an enum constant
        
        Returns:
            OrderStatus -- An enumerated constant representing the order status or None
        """
        try:
            return TokenType[self.type] if self.type else None
        except:
            return None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data.get('id'), json_data.get('type'), json_response= json_data, response_type = response_type)
    
    @classmethod
    def create(cls, token_id: str, token_type: str = TokenType.BILLING_AGREEMENT.name) -> 'Token':
        return cls(token_id, token_type)

class PaymentSource(PayPalEntity):
    """Payment source object representation.
    """
    def __init__(self, card: Card, token: Token, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.card = card
        self.token = token
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        card, token = None, None

        if 'card' in json_data.keys():
            card = Card.serialize_from_json(json_data['card'], response_type)
        if 'token' in json_data.keys():
            token = Token.serialize_from_json(json_data['token'], response_type)
        
        return cls(card, token, json_response= json_data, response_type = response_type)
    
    @classmethod
    def create(cls, card: Card, token: Token) -> 'PaymentSource':
        return cls(card, token)