"""
    Module with basic http constants & session handling
"""

from abc import ABC
from enum import Enum

from datetime import datetime
from typing import NamedTuple

"""
    Live PayPal api base URL.

    This application supports a paypal integration from v2 onwards.
"""
LIVE_API_BASE_URL = 'https://api.paypal.com/v2'

"""
    Sandbox PayPal api base URL.

    This application supports a paypal integration from v2 onwards.
"""
SANDBOX_API_BASE_URL = 'https://api.sandbox.paypal.com/v2'

class SessionType(Enum):
    """
        Enumerated constants for the session type
    """
    BASIC = 1
    TOKEN = 2
    REFRESHABLE = 3

class _PayPalToken(NamedTuple):
    """
        Paypal access token wrapper
    """
    pass

class PayPalSession(ABC):
    """
        PayPal session abstraction
    """
    pass

class _OAuthPayPalSession(PayPalSession):
    """
        PayPal session obj for request with OAuthToken headers.

        A standard session with a finite lifespan,
        once the session is expired this instance will not be valid for further
        requests.
    """
    pass

class _BasicPayPalSession(PayPalSession):
    """
        PayPal session obj for request with Basic Authorization.

        A session with an indefinite lifespan,
        all requests will use basic authorization which means that
        the client & secret will always travel through the network.
    """
    pass

class _RefreshablePayPalSession(PayPalSession):
    """
        PayPal session obj for request with with OAuthToken headers and Basic Authorization.

        A mixed session using the standard _OAuthPayPalSession approach for regular requests
        and a _BasicPayPalSession request to perform a token refresh. This gives the session
        and indefinite lifespan and a limited number of Basic Auth requests with a client &
        secret network roundtrips.
        
        This session can receive flags to limit the refresh count.
    """
    pass

def authenticate(client_id: str, client_secret: str, session_type: SessionType, **kwargs) -> PayPalSession:
    """
        Creates a session for a given user.
        If a session handles any kind of flags it can be received as a kwarg.
        Supported flags: 'refhresh_count' for refreshable sessions.
    """
    pass