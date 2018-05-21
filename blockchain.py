from functools import reduce

import json
import pickle  # python object to binary data
import requests

from block import Block
from transaction import Transaction
from wallet import Wallet

from utility.verification import Verification
from utility.hash_util import hash_block, hash_string_256


""" python store the name of the module in __name__ """
#  MINING_REWARD = 10  # should be given to the people who mined the block


class Blockchain:

    MINING_REWARD = 10  # should be given to the people who mined the block

    def __init__(self, public_key, node_id):
        # Our starting block for blockchain
        genesis_block = Block(0, '', [], 100, 0)
        # Initializing our (empty) blockchain list
        self.chain = [genesis_block]
        # Unhandled transactions
        self.__open_transactions = []
        self.public_key = public_key
        self.__peer_nodes = set()  # every node is unique!
        self.node_id = node_id
        self.need_resolve_conflicts = False
        self.load_data()

    """ Getter """
    @property
    def chain(self):
        """ self.__cahin is automatically created by @property.
        No need to declaire it. """
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
            with open('blockchain-{}.txt'.format(self.node_id), mode='r') as f:
                file_content = f.readlines()
                # :-1 get rid of '\n'
                blockchain = json.loads(file_content[0][:-1])
                updated_blockchain = []
                for block in blockchain:
                    converted_tx = [Transaction(
                        tx['sender'], tx['recipient'], tx['signature'],
                        tx['amount']) for tx in block['transactions']]
                    updated_block = Block(
                        block['index'], block['previous_hash'], converted_tx,
                        block['proof'], block['timestamp'])
                    updated_blockchain.append(updated_block)
                self.chain = updated_blockchain
                open_transactions = json.loads(file_content[1][:-1])
                update_transactions = []
                for tx in open_transactions:
                    updated_transaction = Transaction(
                        tx['sender'], tx['recipient'], tx['signature'],
                        tx['amount'])
                    update_transactions.append(updated_transaction)

                self.__open_transactions = update_transactions
                peer_nodes = json.loads(file_content[2])
                self.__peer_nodes = set(peer_nodes)
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
            with open('blockchain-{}.txt'.format(self.node_id), mode='w') as f:
                saveable_chain = [block.__dict__ for block in
                                  [Block(bl.index, bl.previous_hash,
                                         [tx.__dict__ for tx in
                                          bl.transactions],
                                         bl.proof, bl.timestamp) for bl in
                                   self.__chain]]
                f.write(json.dumps(saveable_chain))
                f.write('\n')
                saveable_tx = [tx.__dict__ for tx in
                               self.__open_transactions]
                f.write(json.dumps(saveable_tx))
                f.write('\n')
                f.write(json.dumps(list(self.__peer_nodes)))
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

    def get_balance(self, sender=None):
        """ Calculate how much a participant send, as well as how much a
        participant received. """
        if sender is None:
            if self.public_key is None:
                return None
            participant = self.public_key
        else:
            participant = sender
        tx_sender = [[tx.amount for tx in block.transactions
                      if tx.sender == participant] for block in self.__chain]
        open_tx_sender = [tx.amount
                          for tx in
                          self.__open_transactions if tx.sender == participant]
        tx_sender.append(open_tx_sender)
        print(tx_sender)
        amount_sent = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0
            else tx_sum+0, tx_sender, 0)

        tx_recipient = [[tx.amount for tx in block.transactions
                         if tx.recipient == participant] for block in
                        self.__chain]
        amount_received = reduce(
            lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0
            else tx_sum+0, tx_recipient, 0)
        # Return the total balance
        return amount_received - amount_sent

    def get_last_blockchain_value(self):
        """ Returns the last value of the current blockchain. """
        if len(self.__chain) < 1:
            return None
        return self.__chain[-1]

    def add_transaction(self, recipient, sender, signature, amount=1.0,
                        is_receiving=False):
        """ Append a new value as well as the last blockchain value to the
        blockchain.

        Arguments:
            :sender: The sender of the coins.
            :recipient: The recipient of the coins.
            :amount: The amount of coins sent with the transaction
            (default = 1.0)
        """
        # if self.public_key == None:
        #     return False
        transaction = Transaction(sender, recipient, signature, amount)
        if Verification.verify_transaction(transaction, self.get_balance):
            self.__open_transactions.append(transaction)
            self.save_data()

            # broadcast results to peer nodes
            if not is_receiving:
                for node in self.__peer_nodes:
                    url = 'http://{}/broadcast-transaction'.format(node)
                    try:
                        response = requests.post(url, json={
                                                 'sender': sender, 'recipient':
                                                 recipient, 'amount': amount,
                                                 'signature': signature})
                        if (response.status_code == 400 or
                                response.status_code == 500):
                            print('Transaction declined, needs resolving')
                            return False
                    except requests.exceptions.ConnectionError:
                        continue    # if a node failed, go through other nodes
            return True
        return False

    def mine_block(self):
        """ Create a new block and add open transactions to it. """
        if self.public_key is None:
            return None
        # Fetch the currently last block of the blockchain
        last_block = self.__chain[-1]
        # Hash the last block (=> to be able to compare it to the stored hash
        # value)
        hashed_block = hash_block(last_block)
        proof = self.proof_of_work()
        # reward_transaction = {
        #     'sender': 'MINING',
        #     'recipient': owner,
        #     'amount': MINING_REWARD
        # }
        reward_transaction = Transaction(
            'MINING', self.public_key, '', self.MINING_REWARD)
        # range selector to make a copy
        copied_transactions = self.__open_transactions[:]
        for tx in copied_transactions:
            if not Wallet.verify_transaction(tx):
                return None
        copied_transactions.append(reward_transaction)
        block = Block(len(self.__chain), hashed_block,
                      copied_transactions, proof)
        self.__chain.append(block)
        self.__open_transactions = []
        self.save_data()
        for node in self.__peer_nodes:
            url = 'http://{}/broadcast-block'.format(node)
            converted_block = block.__dict__.copy()
            converted_block['transactions'] = [
                tx.__dict__ for tx in converted_block['transactions']]
            try:
                response = requests.post(url, json={'block': converted_block})
                if response.status_code == 400 or response.status_code == 500:
                    print('Block declined, needs resolving')
                if response.status_code == 409:
                    self.need_resolve_conflicts = True
            except requests.exceptions.ConnectionError:
                continue
        return block

    def add_block(self, block):
        transactions = [Transaction(
            tx['sender'], tx['recipient'], tx['signature'], tx['amount']) for
            tx in block['transactions']]
        # check ours
        proof_is_valid = Verification.valid_proof(
            transactions[:-1], block['previous_hash'], block['proof'])
        # check peers
        hashes_match = hash_block(self.chain[-1]) == block['previous_hash']
        if not proof_is_valid or not hashes_match:
            return False
        # block is still a dictionary, need to convert first
        converted_block = Block(
            block['index'], block['previous_hash'], transactions,
            block['proof'], block['timestamp'])
        self.__chain.append(converted_block)
        # update open transactions before saving data
        stored_transactions = self.__open_transactions[:]
        for incoming_tx in block['transactions']:
            for opentx in stored_transactions:
                if (opentx.sender == incoming_tx['sender'] and
                    opentx.recipient == incoming_tx['recipient'] and
                    opentx.amount == incoming_tx['amount'] and
                        opentx.signature == incoming_tx['signature']):
                    try:
                        self.__open_transactions.remove(opentx)
                    except ValueError:
                        print('Item was already removed.')
        self.save_data()
        return True

    def resolve(self):
        winner_chain = self.chain
        replace = False
        for node in self.__peer_nodes:
            url = 'http://{}/chain'.format(node)
            try:
                response = requests.get(url)
                node_chain = response.json()
                node_chain = [Block(block['index'], block['previous_hash'],
                                    [Transaction(
                                        tx['sender'], tx['recipient'],
                                        tx['signature'],
                                        tx['amount']) for tx in
                                        block['transactions']],
                                    block['proof'], block['timestamp']) for
                              block in
                              node_chain]
                node_chain_length = len(node_chain)
                local_chain_length = len(winner_chain)
                if (node_chain_length > local_chain_length and
                        Verification.verify_chain(node_chain)):
                    winner_chain = node_chain
                    replace = True
            except requests.exceptions.ConnectionError:
                continue
        self.chain = winner_chain
        self.need_resolve_conflicts = False
        if replace:
            self.__open_transactions = []
        self.save_data()
        return replace

    def add_peer_node(self, node):
        """ Adds a new node to the peer node set.
        Arguments:
            :node: The node URL which should be added.
        """
        self.__peer_nodes.add(node)
        self.save_data()

    def remove_peer_node(self, node):
        """ Removes a node from the peer node set.
        Arguments:
            :node: The node URL which should be removed.
        """
        self.__peer_nodes.discard(
            node)  # using discard(): if no element, do nothing
        self.save_data()

    def get_peer_nodes(self):
        """Return a list of all connected peer nodes."""
        return list(self.__peer_nodes)
