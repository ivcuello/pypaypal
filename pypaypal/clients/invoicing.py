"""
    Invoice api client for paypal REST resources.

    Resource docs & Reference: https://developer.paypal.com/docs/api/invoicing/v2/  
"""

import json
from typing import Type, TypeVar, List

from pypaypal.clients.base import ClientBase
from pypaypal.entities.base import ResponseType, PaypalApiResponse


from pypaypal.http import ( 
    parse_url,
    PayPalSession,     
    LEGACY_LIVE_API_BASE_URL, 
    LEGACY_SANDBOX_API_BASE_URL 
)

"""
    Base Resource Live URL
"""
_LIVE_RESOURCE_BASE_URL = parse_url(LEGACY_LIVE_API_BASE_URL, 'invoices')

"""
    Base Resource Sandbox URL
"""
_SANDBOX_RESOURCE_BASE_URL = parse_url(LEGACY_SANDBOX_API_BASE_URL, 'invoices')
