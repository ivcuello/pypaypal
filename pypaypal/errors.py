"""
    Module containing the client errors and exceptions
"""

class AuthenticationError(Exception):
    """
        Authentication errors
    """
    def __init__(self, response):
        super().__init__('There was an error authenticating the client')
        self.response = response

class ExpiredSessionError(Exception):
    """
        Errors regarding expired tokens & session
    """
    def __init__(self, data):
        super().__init__('token or session has expired')
        self.data = data
    