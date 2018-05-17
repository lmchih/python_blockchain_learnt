from functools import reduce

import json
import pickle  # python object to binary data

from block import Block
from transaction import Transaction
from wallet import Wallet

from utility.verification import Verification
from utility.hash_util import hash_block, hash_string_256


# Initializing our blockchain list
MINING_REWARD = 10  # should be given to the people who mined the block

""" python store the name of the module in __name__ """
# print(__name__)


class Blockchain:
    def __init__(self, hosting_node_id):
        # Our starting block for blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        self.chain = [genesis_block]
        # Unhandled transactions
        self.__open_transactions = []
        self.load_data()
        self.hosting_node = hosting_node_id

    """ Getter """
    @property
    def chain(self):
        """ self.__cahin is automatically created by @property. No need to declare it. """
        return self.__chain[:]  # just retrun a copy

    """ Setter """
    @chain.setter
    def chain(self, val):
        self.__chain = val
        # pass # immutable

    def get_open_transactions(self):
        return self.__open_transactions[:]

    def load_data(self):
        try:
            with open('blockchain.txt', mode='r') as f:
                file_content = f.readlines()
                # :-1 get rid of '\n'
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1])
                update_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'], tx['amount'])
                    update_transactions.append(updated_transaction)

                self.__open_transactions = update_transactions
        except (IOError, IndexError):
            print('Handled exception...')
            pass
        finally:
            print('Cleanup!')

    # Store the blockchain and open transactions to the file
    # This is called whenever we mine a block or add a transaction

    def save_data(self):
        """Save blockchain + open transactions snapshot to a file."""
        try:
            with open('blockchain.txt', mode='w') as f:
                saveable_chain = [block.__dict__ for block in [Block(bl.index, bl.previous_hash, [
                    tx.__dict__ for tx in bl.transactions], bl.proof, bl.timestamp) for bl in self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in
                               self.__open_transactions]
                f.write(json.dumps(saveable_tx))
        except (IOError, IndexError):
            print('Saving Failed!')

    def proof_of_work(self):
        last_block = self.__chain[-1]
        last_hash = hash_block(last_block)
        proof = 0
        while not Verification.valid_proof(
                self.__open_transactions, last_hash, proof):
            proof += 1
        return proof

    def get_balance(self):
        """ Calculate how much a participant send, as well as how much a participant received. """
        participant = self.hosting_node
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount
                          for tx in
                          self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        # print(tx_sender)
        amount_sent = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in self.__chain]
        amount_received = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum+0, tx_recipient, 0)
        # Return the total balance
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0):
        """ Append a new value as well as the last blockchain value to the blockchain. 

        Arguments: 
            :sender: The sender of the coins.
            :recipient: The recipient of the coins. 
            :amount: The amount of coins sent with the transaction (default = 1.0)
        """
        # transaction = {
        #     'sender': sender,
        #     'recipient': recipient,
        #     'amount': amount
        # }]
        if self.hosting_node == None:
            return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()
            return True
        return False

    def mine_block(self):
        """ Create a new block and add open transactions to it. """
        if self.hosting_node == None:
            return False
        # Fetch the currently last block of the blockchain
        last_block = self.__chain[-1]
        # Hash the last block (=> to be able to compare it to the stored hash value)
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction(
            'MINING', self.hosting_node, '', MINING_REWARD)
        # range selector to make a copy
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return False
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        return True
