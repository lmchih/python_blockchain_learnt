import unittest
from wallet import Wallet


class TestWallet(unittest.TestCase):
    def test_create_wallet(self):
        wallet = Wallet(5000)
        self.assertEqual(wallet.node_id, 5000)
        self.assertIsNotNone(wallet)

    def test_load_wallet(self):
        pass


if __name__ == '__main__':
    unittest.main()
