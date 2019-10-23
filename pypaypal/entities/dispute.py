"""
    Module with dispute related entities
"""

from enum import Enum
from datetime import datetime
from typing import Type, List

import dateutil.parser
from pypaypal.entities.base import T, PayPalEntity, ResponseType, ActionLink, Money, PatchUpdateRequest, PaypalMessage, PaypalTransaction

class DisputeUpdateRequest(PatchUpdateRequest):
    """Update request for PATCH dispute updates
    """
    
    def __init__(self, merchant_email:str, note: str, operation: str='add', path: str='/communication_details'):
        super().__init__(path, {'email': merchant_email, 'note': note}, operation)

class DisputeTracker(PayPalEntity):
    """Dispute tracking info
    """
    def __init__(self, tracking_number: str, carrier_name: str, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.carrier_name = carrier_name
        self.tracking_number = tracking_number
        self.tracking_url = kwargs.get('tracking_url')
        self.carrier_name_other = kwargs.get('carrier_name_other')

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['tracking_number'], json_data['carrier_name'],  
            json_response= json_data, response_type = response_type
        )

class DisputeEvidenceInfo(PayPalEntity):
    """Dispute evidence info
    """
    def __init__(self, trackers: List[DisputeTracker], refund_ids: List[str]=[], **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.tracking_info = trackers
        self.refunds_ids = [ {'refund_id': x} for x in refund_ids ]

    def to_dict(self) -> dict:
        d = super().to_dict()
        
        if 'tracking_info' in d.keys():
            d['tracking_info'] = [ e.to_dict() for e in self.tracking_info ]

        return d

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:       
        trackers = [DisputeTracker.serialize_from_json(x) for x in json_data['evidence_info']['tracking_info']]        
    
        return cls(
            trackers, json_data['refund_ids'], json_response= json_data, response_type = response_type
        )

class DisputeEvidence(PayPalEntity):
    """Dispute evidence for requests
    """
    def __init__(self, evidence_type: str, notes: str, item_id: str, evidence_info: DisputeEvidence, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.notes = notes
        self.item_id = item_id
        self.evidence_type = evidence_type
        self.evidence_info = evidence_info
        self.document = {'name' : kwargs['document_name']} if 'document_name' in kwargs.keys() else None

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        return cls(
            json_data['evidence_type'], json_data['notes'], json_data['item_id'], json_data['evidence_info'], 
            json_response= json_data, response_type = response_type
        )

class DisputeOutcome(PayPalEntity):
    """Dispute outcome object representation    
    """
    def __init__(self, outcome_code: str, amount_refunded: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.outcome_code = outcome_code
        self.amount_refunded = amount_refunded

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:
        amount = Money.serialize_from_json(json_data['amount_refunded'])
        
        return cls(
            json_data['outcome_code'], amount, json_response= json_data, response_type = response_type
        )

class Dispute(PayPalEntity):
    """Dispute object representation
    """

    def __init__(self, dispute_id: str, reason: str, status: str, amount: Money, **kwargs):
        super().__init__(kwargs.get('json_response', dict()), kwargs.get('response_type', ResponseType.MINIMAL))
        self.reason = reason
        self.status = status
        self.dispute_id = dispute_id
        self.dispute_amount = amount
        self.offer = kwargs.get('offer')
        self.messages = kwargs.get('messages')
        self.dispute_outcome = kwargs.get('dispute_outcome')
        self.disputed_transactions = kwargs.get('disputed_transactions')
        self.extensions = self._json_response.get('extensions', kwargs.get('extensions')) 
        self._update_time = self._json_response.get('update_time', kwargs.get('update_time')) 
        self._create_time = self._json_response.get('create_time', kwargs.get('create_time')) 
        self.dispute_state = self._json_response.get('dispute_state', kwargs.get('dispute_state')) 
        self.dispute_channel = self._json_response.get('dispute_channel', kwargs.get('dispute_channel')) 
        self.dispute_life_cycle_stage = self._json_response.get('dispute_life_cycle_stage', kwargs.get('dispute_life_cycle_stage'))
        self.links = [ActionLink(x['href'], x['rel'], x.get('method', 'GET')) for x in self._json_response.get('links', [])]

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

    @property
    def read_link(self) -> ActionLink:
        """Retrieves a link to read this entity details.
        
        Returns:
            ActionLink -- The link for requesting the information to the API.
        """
        return next(filter(lambda x: x.rel == 'self', self.links), None)

    @classmethod
    def serialize_from_json(cls: Type[T], json_data: dict, response_type: ResponseType = ResponseType.MINIMAL) -> T:        
        amount = Money.serialize_from_json(json_data['dispute_amount'])
        offer, dispute_outcome, messages, disputed_transactions = None, None, [], []

        if 'offer' in json_data.keys():
            offer = Money.serialize_from_json(json_data['offer'], response_type)
        
        if 'dispute_outcome' in json_data.keys():
            dispute_outcome = DisputeOutcome.serialize_from_json(json_data['dispute_outcome'], response_type)

        if 'messages' in json_data.keys():
            messages = [ PaypalMessage.serialize_from_json(x, response_type) for x in json_data['messages'] ]

        if 'disputed_transactions' in json_data.keys():
            disputed_transactions = [ PaypalTransaction.serialize_from_json(x, response_type) for x in json_data['disputed_transactions'] ]

        return cls(
            json_data['dispute_id'], json_data['reason'], json_data['status'], amount, json_response= json_data, 
            response_type = response_type, offer = offer, dispute_outcome = dispute_outcome, messages = messages, 
            disputed_transactions = disputed_transactions
        )
