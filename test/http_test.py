"""Test module for main http module 
"""

import os
import unittest

from pypaypal.errors import IdentityError, ExpiredSessionError

from pypaypal.http import ( 
    AuthType,
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
        self.auth_session = None
        self.token_session = None
        self.disposable_session = None
        self.auth_type = AuthType.TOKEN
        self.client = os.environ['TEST_PP_CLIENT']
        self.secret = os.environ['TEST_PP_SECRET']
    
    def tearDown(self):
        self.client = None
        self.secret = None
        self.auth_session = None
        self.token_session = None
        self.disposable_session = None
    
    def test_authentication(self):
        try:
            authenticate(self.client, 'invalid-secret', _MODE, self.auth_type)
            raise AssertionError('An IdentityError was expected.')
        except IdentityError:
            print('IdentityError test OK!!')

        self.auth_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
        self.assertEqual(self.auth_session.status, SessionStatus.ACTIVE)

        self.token_session = session_from_token(self.auth_session._paypal_token, _MODE)
        self.assertEqual(self.token_session.status, SessionStatus.ACTIVE)

        self.disposable_session = session_from_token(self.auth_session._paypal_token, _MODE)
        self.assertEqual(self.disposable_session.status, SessionStatus.ACTIVE)

    def test_session_expiration(self):
        pass

    def test_disposability(self):
        test_disposability(self.disposable_session)
        self.assertEqual(self.disposable_session.status, SessionStatus.DISPOSED)
    
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
        self.auth_session = None
        self.disposable_session = None
        self.auth_type = AuthType.BASIC
        self.client = os.environ['TEST_PP_CLIENT']
        self.secret = os.environ['TEST_PP_SECRET']
    
    def tearDown(self):
        self.client = None
        self.secret = None
        self.auth_session = None
        self.disposable_session = None
    
    def test_authentication(self):
        try:
            authenticate(self.client, 'invalid-secret', _MODE, self.auth_type)
            raise AssertionError('An IdentityError was expected.')
        except IdentityError:
            print('IdentityError test OK!!')

        self.auth_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
        self.assertEqual(self.auth_session.status, SessionStatus.ACTIVE)

        self.disposable_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
        self.assertEqual(self.disposable_session.status, SessionStatus.ACTIVE)

    def test_session_expiration(self):
        pass

    def test_disposability(self):
        test_disposability(self.disposable_session)
        self.assertEqual(self.disposable_session.status, SessionStatus.DISPOSED)
    
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
        self.auth_session = None
        self.disposable_session = None
        self.auth_type = AuthType.REFRESHABLE
        self.client = os.environ['TEST_PP_CLIENT']
        self.secret = os.environ['TEST_PP_SECRET']
    
    def tearDown(self):
        self.client = None
        self.secret = None
        self.auth_session = None
        self.disposable_session = None
    
    def test_authentication(self):
        try:
            authenticate(self.client, 'invalid-secret', _MODE, self.auth_type)
            raise AssertionError('An IdentityError was expected.')
        except IdentityError:
            print('IdentityError test OK!!')

        self.auth_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
        self.assertEqual(self.auth_session.status, SessionStatus.ACTIVE)

        self.disposable_session = authenticate(self.client, self.secret, _MODE, self.auth_type)
        self.assertEqual(self.disposable_session.status, SessionStatus.ACTIVE)

    def test_session_expiration(self):
        pass

    def test_disposability(self):
        test_disposability(self.disposable_session)
        self.assertEqual(self.disposable_session.status, SessionStatus.DISPOSED)
    
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

if __name__ == '__main__':
    unittest.main()