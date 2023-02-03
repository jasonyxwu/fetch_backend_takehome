import unittest
import random
from spendpoints import Account
class TestSpendPointus(unittest.TestCase):
  def test_numbers(self):
    for i in range (10000):
      spending = random.randint(-1000, 20000)
      new_account = Account()
      new_account.read_data()
      new_account.spend_points(spending)

if __name__ == '__main__':
    unittest.main()