"""test module for pypaypal.entities.base
"""

import unittest

from pypaypal.entities.base import ApplicationContext

# TODO: Write tests here
class ApplicationContextTests(unittest.TestCase):
    
    def setUp(self):
        self.sample_data = {
            'brand_name': 'brand', 'locale': 'es', 'landing_page': 'NONE', 
            'shipping_preference': 'NO_SHIPPING', 'user_action': 'NONE', 
            'payment_method': 'CREDIT_CARD', 'return_url': '-', 
            'cancel_url': '-'
        }
    
    def test_creation_positional(self):
        """Create factory method should not raise errors with position args"""
        ApplicationContext.create(
            self.sample_data['brand_name'], self.sample_data['locale'], 
            self.sample_data['landing_page'], self.sample_data['shipping_preference'],
            self.sample_data['user_action'], self.sample_data['payment_method'], 
            self.sample_data['return_url'], self.sample_data['cancel_url']
        )
    
    def test_creation_keyworded(self):
        """Create factory method should not raise errors with keyword args"""
        ApplicationContext.create(**self.sample_data)

if __name__ == '__main__':
    unittest.main()
