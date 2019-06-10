import unittest # import to performe tests
from Blackjack import ranks, values

class testCardValue(unittest.TestCase):
    def test_value(self):
        # test all values of cards in deck
        self.assertAlmostEqual(11, values['Ace']) # (what is expected, what is given)