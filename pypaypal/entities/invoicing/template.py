"""
    Module with invoice templete related entities
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser

from pypaypal.entities.base import ( 
    T,
    Item,   
    Money,
    ActionLink,
    PayPalEntity,
    ResponseType,
    RecipientInfo
)

from pypaypal.entities.invoicing.base import (
    MetaData,
    InvoicerInfo,
    FileReference,
    PartialPayment,
    AmountSummaryDetail
)

class InvoiceListRequestField(Enum):
    ALL = 1
    NONE = 2

class PmtTermType(Enum):
    #  The payment for the invoice is due upon receipt of the invoice.
    DUE_ON_RECEIPT = 1
    #  The payment for the invoice is due on the date specified in the invoice.
    DUE_ON_DATE_SPECIFIED = 2
    #  The payment for the invoice is due in 10 days.
    NET_10 = 3
    #  The payment for the invoice is due in 15 days.
    NET_15 = 4
    #  The payment for the invoice is due in 30 days.
    NET_30 = 5
    #  The payment for the invoice is due in 45 days.
    NET_45 = 6
    #  The payment for the invoice is due in 60 days.
    NET_60 = 7
    #  The payment for the invoice is due in 90 days.
    NET_90 = 8
    #  The invoice has no payment due date.    
    NO_DUE_DATE = 9

class PaymentTermType(PayPalEntity):
    """PaymentTermType obj representation
    """
    def __init__(self, term_type: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.term_type = term_type
    
    @property
    def term_type_enum(self) -> PmtTermType:
        return PmtTermType[self.term_type]

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data)
        return cls(**args, json_response= json_data, response_type = response_type)

class TemplateDetail(PayPalEntity):
    """Template detail object representation.
    """

    _ARRAY_TYPES = { 'attachments': FileReference }
    _ENTITY_TYPES = { 'metadata': MetaData, 'payment_term': PaymentTermType }

    def __init__(
        self, reference: str, currency_code: str, note: str, 
        terms_and_conditions: str, memo: str, payment_term: PaymentTermType,
        metadata: MetaData = None, attachments: List[FileReference] = [],
        **kwargs
    ):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.reference = reference
        self.currency_code = currency_code
        self.note = note
        self.terms_and_conditions = terms_and_conditions
        self.memo = memo
        self.payment_term = payment_term
        self.metadata = metadata
        self.attachments = attachments or []

    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.metadata:
            ret['metadata'] = [ x.to_dict() for x in self.metadata ]
        if self.attachments:
            ret['attachments'] = [ x.to_dict() for x in self.attachments ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES, cls._ARRAY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

    @classmethod
    def create(
        cls, currency_code: str, *, reference: str, note: str, 
        terms_and_conditions: str, memo: str, payment_term: str, 
        metadata: MetaData, attachments: List[FileReference] = []
    ):
        return cls(
            reference, currency_code, note, terms_and_conditions, 
            memo, payment_term, metadata, attachments or []
        )

class TemplateConfiguration(PayPalEntity):
    """Invoice configuration object representation
    """

    _ENTITY_TYPES = {'partial_payment': PartialPayment}

    def __init__(self, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.allow_tip: bool = kwargs.get('allow_tip', False)
        self.tax_inclusive: bool = kwargs.get('tax_inclusive', False)
        self.partial_payment: PartialPayment = kwargs.get('partial_payment', None)
        self.tax_calculated_after_discount: bool = kwargs.get('tax_calculated_after_discount', True)
    
    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

    @classmethod
    def create(
        cls, *, tax_calculated_after_discount: bool = True, tax_inclusive: bool = False,
        allow_tip: bool = False, partial_payment: PartialPayment=None
    ):
        return cls(
            tax_calculated_after_discount=tax_calculated_after_discount,
            tax_inclusive=tax_inclusive, allow_tip=allow_tip, 
            partial_payment=partial_payment
        )

class TemplateInfo(PayPalEntity):
    """Template info object representation. 
        Includes invoicer business information, invoice recipients,
        items, and configuration.
    """
    
    _ARRAY_TYPES = { 'items': Item, 'primary_recipients': RecipientInfo }

    _ENTITY_TYPES = {
        'detail': TemplateDetail, 'invoicer': InvoicerInfo,
        'configuration': TemplateConfiguration, 'amount': AmountSummaryDetail, 'due_amount': Money
    }

    def __init__(self, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.due_amount: Money = kwargs.get('due_amount')
        self.detail: TemplateDetail = kwargs.get('detail')
        self.invoicer: InvoicerInfo = kwargs.get('invoicer')
        self.amount: AmountSummaryDetail = kwargs.get('amount')
        self.configuration: TemplateConfiguration = kwargs.get('configuration')
        self.items: List[Item] = kwargs.get('items', [])
        self.primary_recipients: List[RecipientInfo] = kwargs.get('primary_recipients')        
        self.additional_recipients = self._json_response.get('additional_recipients', kwargs.get('additional_recipients'))
    
    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.items:
            ret['items'] = [ x.to_dict() for x in self.items ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES, cls._ARRAY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

    @classmethod
    def create(
        cls: Type[T], *, detail: TemplateDetail, invoicer: InvoicerInfo, primary_recipients: List[RecipientInfo], 
        additional_recipients: List[str], items: List[Item], configuration: TemplateConfiguration, amount: AmountSummaryDetail,
        due_amount: Money = None)  -> 'TemplateInfo':

        add_rep = [{ 'email_address': x} for x in additional_recipients]

        return cls(
            detail=detail, invoicer=invoicer, primary_recipients=primary_recipients, 
            items=items, configuration=configuration, amount=amount, due_amount=due_amount, 
            additional_recipients = add_rep
        )

class DisplayPreference(PayPalEntity):
    """Display preference object representation
    """
    def __init__(self, hidden: bool, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.hidden = hidden

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(json_data['hidden'], json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, hidden: bool) -> 'DisplayPreference':
        return cls(hidden)

class TemplateItemSetting(PayPalEntity):
    """Template item setting object representation
    """
    
    _ENTITY_TYPES = {'display_preference': DisplayPreference}

    def __init__(self, field_name: str, display_preference: DisplayPreference, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.field_name = field_name
        self.display_preference = display_preference

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, field_name: str, hidden: bool = False) -> 'TemplateItemSetting':
        return cls(field_name, DisplayPreference.create(hidden))

class TemplateSubtotalSetting(PayPalEntity):
    """Template subtotal setting object representation
    """

    _ENTITY_TYPES = {'display_preference': DisplayPreference}

    def __init__(self, field_name: str, display_preference: DisplayPreference, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.field_name = field_name
        self.display_preference = display_preference

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, field_name: str, hidden: bool = False) -> 'TemplateSubtotalSetting':
        return cls(field_name, DisplayPreference.create(hidden))

class TemplateSettings(PayPalEntity):
    """Template show/hide settings object representation.
    """
    _ARRAY_TYPES = { 
        'template_item_settings': TemplateItemSetting, 
        'template_subtotal_settings': TemplateSubtotalSetting 
    }

    def __init__(self, 
        template_item_settings: List[TemplateItemSetting], 
        template_subtotal_settings: List[TemplateSubtotalSetting], **kwargs
        ):
            super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
            self.template_item_settings = template_item_settings
            self.template_subtotal_settings = template_subtotal_settings
    
    def to_dict(self) -> dict:
        ret = super().to_dict()        
        if self.template_item_settings:
            ret['template_item_settings'] = [ x.to_dict() for x in self.template_item_settings ]
        if self.template_subtotal_settings:
            ret['template_subtotal_settings'] = [ x.to_dict() for x in self.template_subtotal_settings ]
        return ret

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data=json_data, array_types=cls._ARRAY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

    @classmethod
    def create(cls, field_name: str, hidden: bool = False) -> 'TemplateSubtotalSetting':
        return cls(field_name, DisplayPreference.create(hidden))

class Template(PayPalEntity):
    """Invoice template object representation    
    """

    _ENTITY_TYPES = { 'template_info': TemplateInfo, 'settings': TemplateSettings }

    def __init__(
        self, default_template: bool, 
        template_info: TemplateInfo, settings: TemplateSettings, 
        unit_of_measure: str, name: str = None, **kwargs
        ):
            super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
            self.name = name
            self.settings = settings
            self.template_info = template_info
            self.unit_of_measure = unit_of_measure
            self.default_template = default_template
            self.id = self._json_response.get('id', kwargs.get('id'))
            self.standard_template = self._json_response.get('standard_template', kwargs.get('standard_template'))
            self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @property
    def replace_link(self) -> ActionLink:
        """Retrieves a link to replace (update) this template.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'replace', self.links), None)

    @property
    def delete_link(self) -> ActionLink:
        """Retrieves a link to delete this template.
        
        Returns:
            ActionLink -- The link to execute the API action.
        """
        return next(filter(lambda x: x.rel == 'delete', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        args = super()._build_args(json_data, cls._ENTITY_TYPES)
        return cls(**args, json_response= json_data, response_type = response_type)

    @classmethod
    def create(
            cls, name: str, template_info: TemplateInfo, settings: TemplateSettings, 
            unit_of_measure: str, default_template: bool = False
        ) -> 'Template':
            return cls(default_template, template_info, settings, unit_of_measure, name=name)