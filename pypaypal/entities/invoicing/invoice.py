"""
    Module with invoice related entities
"""

from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import ( 
    T, 
    Item,
    Refund,
    DateRange,
    ActionLink, 
    AmountRange, 
    PayPalEntity, 
    ResponseType, 
    Money,
    RecipientInfo    
)

from pypaypal.entities.invoicing.base import ( 
    MetaData, 
    ShippingCost,
    InvoicerInfo, 
    FileReference, 
    PartialPayment,
    AmountSummaryDetail
)

from pypaypal.entities.invoicing.template import Template

class InvoicePaymentTerm(PayPalEntity):
    """Invoice payment term object representation
    """

    def __init__(self, term_type: str, due_date: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self._due_date = due_date
        self.term_type = term_type
    
    @property
    def due_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._due_date) if self._due_date else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['due_date'] = ret.pop('_due_date', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['term_type'], json_data['due_date'], json_response= json_data, response_type = response_type
        )

    @classmethod
    def create(cls, term_type: str, due_date: datetime):
        return cls(term_type, due_date.strftime('%Y-%m-%d'))

class InvoiceDetail(PayPalEntity):
    """Invoice detail object representation
    """

    def __init__(
        self, currency_code: str, invoice_number: str, metadata: MetaData,
        payment_term: InvoicePaymentTerm=None, attachments: List[FileReference]= [],
         **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.metadata = metadata
        self.payment_term = payment_term
        self.currency_code = currency_code
        self.invoice_number = invoice_number
        self.attachments = attachments or []
        self.note = self._json_response.get('note', kwargs.get('note'))
        self.memo = self._json_response.get('memo', kwargs.get('memo'))
        self.reference = self._json_response.get('reference', kwargs.get('reference'))        
        self._invoice_date = self._json_response.get('invoice_date', kwargs.get('invoice_date'))
        self.terms_and_conditions = self._json_response.get('terms_and_conditions', kwargs.get('terms_and_conditions'))

    @property
    def invoice_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._invoice_date) if self._invoice_date else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['invoice_date'] = ret.pop('_invoice_date', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        metadata, payment_term, attachments = None, None, []

        if 'metadata' in json_data.keys():
            metadata =  MetaData.serialize_from_json(json_data['metadata'], response_type)        
        if 'payment_term' in json_data.keys():
            payment_term = InvoicePaymentTerm.serialize_from_json(json_data['payment_term'], response_type)
        
        if 'attachments' in json_data.keys():
            attachments = [FileReference.serialize_from_json(x, response_type) for x in json_data['attachments']]

        return cls(
            json_data['currency_code'], json_data['invoice_number'], metadata, 
            payment_term, attachments, json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(
        cls, currency_code: str, invoice_number: str, metadata: MetaData, *, 
        payment_term: InvoicePaymentTerm=None, attachments: List[FileReference]= [],
        note:str = None, memo:str = None, reference:str = None, invoice_date: datetime = None, 
        terms_and_conditions: str = None
    ):
        return cls(
            currency_code, invoice_number, metadata, payment_term, 
            attachments or [], note = note, memo = memo, reference = reference, 
            invoice_date = invoice_date, terms_and_conditions = terms_and_conditions
        )

class InvoiceConfiguration(PayPalEntity):
    """Invoice configuration object representation
    """

    def __init__(self, template_id: str, tax_calc_after_discount: bool, tax_inclusive: bool, allow_tip: bool, partial_payment: PartialPayment=None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.allow_tip = allow_tip
        self.template_id = template_id
        self.tax_inclusive = tax_inclusive
        self.partial_payment = partial_payment
        self.tax_calc_after_discount = tax_calc_after_discount

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        partial_payment = PartialPayment.serialize_from_json(json_data['partial_payment']) if 'partial_payment' in json_data.keys() else None

        return cls(
            json_data.get('template_id'), json_data.get('tax_calc_after_discount'), json_data.get('tax_inclusive'),
            json_data.get('allow_tip'), partial_payment, json_response= json_data, response_type = response_type
        )
    
    @classmethod
    def create(
        cls, *, template_id: str = None, tax_calc_after_discount: bool = True, 
        tax_inclusive: bool = False, allow_tip: bool = False, partial_payment: PartialPayment=None
    ):
        return cls(template_id, tax_calc_after_discount, tax_inclusive, allow_tip, partial_payment)

class PaymentDetail(PayPalEntity):
    """Payment object representation for invoice draft
    """
    def __init__(self, pd_type: str, payment_id: str, method: str, amount: Money = None, shipping_info: ShippingCost= None, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.type = pd_type
        self.method = method
        self.amount = amount
        self.payment_id = payment_id
        self.shipping_info = shipping_info
        self.note = self._json_response.get('note', kwargs.get('note'))
        self._payment_date = self._json_response.get('payment_date', kwargs.get('payment_date'))

    @property
    def payment_date(self) -> datetime:
        try:
            return dateutil.parser.parse(self._payment_date) if self._payment_date else None
        except:
            return None

    def to_dict(self) -> dict:
        ret = super().to_dict()
        ret['payment_date'] = ret.pop('_payment_date', None)
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount, shipping = None, None
        
        if 'amount' in json_data.keys():
            amount = Money.serialize_from_json(json_data['amount'])
        if 'shipping_info' in json_data.keys():
            shipping = ShippingCost.serialize_from_json(json_data['shipping_info'])

        return cls(json_data['pd_type'], json_data['payment_id'], json_data['method'], 
                    amount, shipping, json_response= json_data, response_type = response_type
            )
        
    @classmethod
    def create(cls, *, payment_id: str, method: str, note: str, payment_date: datetime, amount: Money, shipping_info: ShippingCost) -> T:
        return cls(None, payment_id, method, amount, shipping_info, note = note, payment_date = payment_date.strftime('%Y-%m-%d'))

class InvoicePayment(PayPalEntity):
    """Payment object representation for invoice draft
    """
    def __init__(self, paid_amount: Money, transactions: List[PaymentDetail], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.paid_amount = paid_amount
        self.transactions = transactions

    def to_dict(self) -> dict:
        ret = super().to_dict()
        if self.transactions:
            ret['transactions'] = [ x.to_dict() for x in self.transactions ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        paid_amount, transactions = None, list()

        if 'paid_amount' in json_data.keys():
            paid_amount = Money.serialize_from_json(json_data['paid_amount'], response_type)        
        if 'transactions' in json_data.keys():
            transactions = [PaymentDetail.serialize_from_json(x, response_type) for x in json_data['transactions']]
        
        return cls(paid_amount, transactions, json_response= json_data, response_type = response_type)

class Invoice(PayPalEntity):
    """Object representation for a paypal invoice
    """    
 
   # Serializable paypal entity arrays
    _ARRAY_TYPES = { 
        'primary_recipients': RecipientInfo, 'payments': InvoicePayment,
        'items': Item, 'refunds': Refund, 'templates': Template
    }

    # Serializable simple paypal entities
    _ENTITY_TYPES = { 
        'due_amount': Money, 'gratuity': Money,
        'detail': InvoiceDetail, 'invoicer': InvoicerInfo, 
        'configuration': InvoiceConfiguration, 'amount': AmountSummaryDetail
    }
 
    def __init__(self,  **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.id: str = kwargs.get('id', None)
        self.gratuity: Money = kwargs.get('gratuity', None)
        self.due_amount: Money = kwargs.get('due_amount', None)
        self.detail: InvoiceDetail = kwargs.get('detail', None)
        self.invoicer: InvoicerInfo = kwargs.get('invoicer', None)
        self.amount: AmountSummaryDetail = kwargs.get('amount', None)
        self.configuration: InvoiceConfiguration = kwargs.get('configuration', None)
        self.items: List[Item] = kwargs.get('items', [])
        self.refunds: List[Refund] = kwargs.get('refunds', [])
        self.templates: List[Template] = kwargs.get('templates', [])
        self.payments: List[InvoicePayment] = kwargs.get('payments', [])
        self.primary_recipients: List[RecipientInfo] = kwargs.get('primary_recipients', [])
        self.status = self._json_response.get('status', kwargs.get('status'))
        self.additional_recipients = self._json_response.get('additional_recipients', kwargs.get('additional_recipients'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @property
    def send_link(self) -> ActionLink:
        """Retrieves a link to send this draft and creating an invoice from it.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'send', self.links), None)

    @property
    def replace_link(self) -> ActionLink:
        """Retrieves a link to replace (update) this draft.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'replace', self.links), None)

    @property
    def delete_link(self) -> ActionLink:
        """Retrieves a link to delete this draft.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'delete', self.links), None)

    @property
    def record_payment_link(self) -> ActionLink:
        """Retrieves a link to record a payment on this draft.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'record-payment', self.links), None)

    @property
    def gen_qr_code_link(self) -> ActionLink:
        """Retrieves a link to generate a qr-code for this draft.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'qr-code', self.links), None)

    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.items:
            ret['items'] = [ x.to_dict() for x in self.items ]
        if self.refunds:
            ret['refunds'] = [ x.to_dict() for x in self.refunds ]
        if self.payments:
            ret['payments'] = [ x.to_dict() for x in self.payments ]
        if self.primary_recipients:
            ret['primary_recipients'] = [ x.to_dict() for x in self.primary_recipients ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES, cls._ARRAY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls: Type[T], *, detail: InvoiceDetail, invoicer: InvoicerInfo, primary_recipients: List[RecipientInfo], 
        additional_recipients: List[str], items: List[Item], configuration: InvoiceConfiguration, amount: Money, 
        payments: List[InvoicePayment], refunds: List[Refund], due_amount: Money = None, gratuity: Money = None)  -> T:

        add_rep = [{ 'email_address': x} for x in additional_recipients]

        return cls(
            id= None, detail=detail, invoicer=invoicer, primary_recipients= primary_recipients,
            items=items, configuration=configuration, amount=amount, payments=payments, 
            refunds=refunds, due_amount=due_amount, gratuity=gratuity, additional_recipients = add_rep
        )

class InvoiceSearchRequest:
    """Search request for invoice queries
    """

    def __init__(
        self, email: str, recipient_first_name: str, recipient_last_name: str,
        recipient_business_name: str, inv_status: List[str], invoice_number: str, reference: str,
        country_code: str, memo: str, total_amount_range: AmountRange, invoice_date_range: DateRange,
        due_date_range: DateRange, payment_date_range: DateRange, creation_date_range: DateRange, archived: bool,
        fields: List[str]
    ):
        self.email = email
        self.recipient_first_name = recipient_first_name
        self.recipient_last_name = recipient_last_name
        self.recipient_business_name = recipient_business_name
        self.inv_status = inv_status
        self.invoice_number = invoice_number
        self.reference = reference
        self.country_code = country_code
        self.memo = memo
        self.total_amount_range = total_amount_range
        self.invoice_date_range     = invoice_date_range
        self.due_date_range = due_date_range
        self.payment_date_range = payment_date_range
        self.creation_date_range = creation_date_range
        self.archived = archived
        self.fields = fields
    
    def to_dict(self) -> dict:
        d = {
            'email' : self.email,
            'recipient_first_name' : self.recipient_first_name,
            'recipient_last_name' : self.recipient_last_name,
            'recipient_business_name' : self.recipient_business_name,
            'inv_status' : self.inv_status,
            'invoice_number' : self.invoice_number,
            'reference' : self.reference,
            'country_code' : self.country_code,
            'memo' : self.memo,
            'total_amount_range' : self.total_amount_range.to_dict(),
            'invoice_date_range' : self.invoice_date_range.to_dict(),
            'due_date_range' : self.due_date_range.to_dict(),
            'payment_date_range' : self.payment_date_range.to_dict(),
            'creation_date_range' : self.creation_date_range.to_dict(),
            'archived' : self.archived,
            'fields' : self.fields
        }

        return { k:v for k,v in d.items() if v != None }
    
    @classmethod
    def create(
        cls, *, email: str = None, recipient_first_name: str = None, recipient_last_name: str = None,
        recipient_business_name: str = None, inv_status: List[str] = None, invoice_number: str = None, reference: str = None,
        country_code: str = None, memo: str = None, total_amount_range: AmountRange = None, invoice_date_range: DateRange = None,
        due_date_range: DateRange = None, payment_date_range: DateRange = None, creation_date_range: DateRange = None, archived: bool = None,
        fields: List[str] = None
    ):
        return cls(
            email, recipient_first_name, recipient_last_name, recipient_business_name, inv_status, invoice_number, reference,
            country_code, memo, total_amount_range, invoice_date_range, due_date_range, payment_date_range, creation_date_range, 
            archived, fields
        )