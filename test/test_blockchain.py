import unittest
from mock import MagicMock
from wallet import Wallet
from block import Block
from blockchain import Blockchain
from transaction import Transaction


class TestBlockchain(unittest.TestCase):
    def test_mine_block(self):
        wallet = Wallet(5000)
        wallet.load_keys()
        blockchain = Blockchain(wallet.public_key, wallet.node_id)
        blockchain.load_data()

        old_balance = blockchain.get_balance()
        blockchain.mine_block()
        self.assertEqual(blockchain.get_balance(), old_balance +
                         Blockchain.MINING_REWARD)

    def test_add_transaction(self):
        pass

    def test_add_peer_node(self):
        wallet = Wallet(5000)
        wallet.load_keys()
        blockchain = Blockchain(wallet.public_key, wallet.node_id)
        blockchain.load_data()
        adding_node = 'localhost:5001'
        blockchain.add_peer_node(adding_node)
        self.assertTrue(adding_node in blockchain.get_peer_nodes())

    def test_delete_peer_node(self):
        wallet = Wallet(5000)
        wallet.load_keys()
        blockchain = Blockchain(wallet.public_key, wallet.node_id)
        blockchain.load_data()
        try:
            deleting_node = blockchain.get_peer_nodes()[0]
            blockchain.remove_peer_node(deleting_node)
            self.assertTrue(
                deleting_node not in blockchain.get_peer_nodes())
        except(IndexError):
            print('There are no peer nodes.')


# print(__name__)
if __name__ == '__main__':
    print('Start testing {}'.format(__file__))
    print('-' * 70)
    unittest.main()
