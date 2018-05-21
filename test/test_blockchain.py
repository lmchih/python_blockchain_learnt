import unittest
from mock import MagicMock
from wallet import Wallet
from block import Block
from blockchain import Blockchain
from transaction import Transaction

# from utility.hash_util import hash_block, hash_string_256


class TestBlockchain(unittest.TestCase):
    def test_mine_block(self):
        wallet = Wallet(5000)
        wallet.load_keys()
        blockchain = Blockchain(wallet.public_key, wallet.node_id)
        blockchain.load_data()

        ori_balance = blockchain.get_balance()
        blockchain.mine_block()
        self.assertEqual(blockchain.get_balance(), ori_balance + 10)

    def test_add_transaction(self):
        pass

    def test_add_peer_node(self):
        pass


# print(__name__)
if __name__ == '__main__':
    print('Start testing {}'.format(__file__))
    print('-' * 70)
    unittest.main()
