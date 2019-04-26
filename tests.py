import unittest
from PizzaScript import *

class TestAll(unittest.TestCase):
    
    def test_get_users_returns_users(self):
        self.assertIsNotNone(getUsers())

    def test_check_match_returns_all_matches(self):
        users = [['Ramzi'], ['Alex'], ['Boden']]
        tweet = 'ramZi wins pizza! Also Boden.'
        print checkMatch(users, tweet)
        self.assertEquals(checkMatch(users, tweet), [['Ramzi'], ['Boden']])

if __name__ == '__main__':
    unittest.main()