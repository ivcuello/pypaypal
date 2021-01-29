"""Integration Test module for main http module 
   it's required to provide client & secret 
   ENV variables for this tests executions
"""

import os
import unittest

from pypaypal.errors import IdentityError, ExpiredSessionError

from pypaypal.http import ( 
    AuthType,
    parse_url,
    SessionMode,
    PayPalSession,
    SessionStatus,
    authenticate, 
    session_from_token
)

_MODE = SessionMode.SANDBOX

def test_disposability(session :PayPalSession):
    try:
        with session:
            pass
        session.get('https://api.sandbox.paypal.com/v2/payments/authorizations/6W688518YP6703149')
        raise AssertionError('This must be unreachable')
    except ExpiredSessionError:
        print('Expired session test OK!!')

class TestOAuthSession(unittest.TestCase):
    """Test class for OAuthSession implementation
    """    
    def setUp(self):
        self.auth_type = AuthType.TOKEN
        self.client = os.environ['TEST_PP_CLIENT']
        self.secret = os.environ['TEST_PP_SECRET']
        self.auth_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
    
    def tearDown(self):
        self.client = None
        self.secret = None
        self.auth_session = None
    
    def test_invalid_authentication(self):
        try:
            authenticate(self.client, 'invalid-secret', _MODE, self.auth_type)
            raise AssertionError('An IdentityError was expected.')
        except IdentityError:
            print('IdentityError test OK!!')

    def test_authentication(self):
        auth_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
        self.assertEqual(auth_session.status, SessionStatus.ACTIVE)

    def test_session_from_token(self):
        token_session = session_from_token(self.auth_session._paypal_token, _MODE)
        self.assertEqual(token_session.status, SessionStatus.ACTIVE)

    def test_disposability(self):
        disposable_session = session_from_token(self.auth_session._paypal_token, _MODE)
        self.assertEqual(disposable_session.status, SessionStatus.ACTIVE)
        test_disposability(disposable_session)
        self.assertEqual(disposable_session.status, SessionStatus.DISPOSED)

    def test_session_expiration(self):
        pass

    def test_post(self):
        pass

    def test_get(self):
        pass
    
    def test_put(self):
        pass
    
    def test_patch(self):
        pass
    
    def test_delete(self):
        pass

class TestBasicSession(unittest.TestCase):
    """Test class for BasicSession implementation
    """
    def setUp(self):        
        self.auth_type = AuthType.BASIC
        self.client = os.environ['TEST_PP_CLIENT']
        self.secret = os.environ['TEST_PP_SECRET']
        self.auth_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
    
    def tearDown(self):
        self.client = None
        self.secret = None
        self.auth_session = None
    
    def test_invalid_authentication(self):
        try:
            authenticate(self.client, 'invalid-secret', _MODE, self.auth_type)
            raise AssertionError('An IdentityError was expected.')
        except IdentityError:
            print('IdentityError test OK!!')

    def test_authentication(self):
        auth_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
        self.assertEqual(auth_session.status, SessionStatus.ACTIVE)

    def test_session_from_token(self):
        token_session = session_from_token(self.auth_session._paypal_token, _MODE)
        self.assertEqual(token_session.status, SessionStatus.ACTIVE)

    def test_disposability(self):
        disposable_session = session_from_token(self.auth_session._paypal_token, _MODE)
        self.assertEqual(disposable_session.status, SessionStatus.ACTIVE)
        test_disposability(disposable_session)
        self.assertEqual(disposable_session.status, SessionStatus.DISPOSED)

    def test_session_expiration(self):
        pass
    
    def test_post(self):
        pass

    def test_get(self):
        pass
    
    def test_put(self):
        pass
    
    def test_patch(self):
        pass
    
    def test_delete(self):
        pass

class TestRefreshableSession(unittest.TestCase):
    """Test class for RefreshableSession implementation
    """
    def setUp(self):
        self.auth_type = AuthType.REFRESHABLE
        self.client = os.environ['TEST_PP_CLIENT']
        self.secret = os.environ['TEST_PP_SECRET']
        self.auth_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
    
    def tearDown(self):
        self.client = None
        self.secret = None
        self.auth_session = None

    def test_invalid_authentication(self):
        try:
            authenticate(self.client, 'invalid-secret', _MODE, self.auth_type)
            raise AssertionError('An IdentityError was expected.')
        except IdentityError:
            print('IdentityError test OK!!')

    def test_authentication(self):
        auth_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
        self.assertEqual(auth_session.status, SessionStatus.ACTIVE)

    def test_session_from_token(self):
        token_session = session_from_token(self.auth_session._paypal_token, _MODE)
        self.assertEqual(token_session.status, SessionStatus.ACTIVE)

    def test_disposability(self):
        disposable_session = session_from_token(self.auth_session._paypal_token, _MODE)
        self.assertEqual(disposable_session.status, SessionStatus.ACTIVE)
        test_disposability(disposable_session)
        self.assertEqual(disposable_session.status, SessionStatus.DISPOSED)

    def test_session_expiration(self):
        pass
    
    def test_post(self):
        pass

    def test_get(self):
        pass
    
    def test_put(self):
        pass
    
    def test_patch(self):
        pass
    
    def test_delete(self):
        pass

class TestModuleMethods(unittest.TestCase):

    def test_parse_url(self):
        """url parsing function test
        """
        expected = 'https://api.sandbox.paypal.com/v2/billing/subscriptions'
        actual = parse_url('https://api.sandbox.paypal.com/v2', 'billing', '/subscriptions')
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()