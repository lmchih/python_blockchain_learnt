""" Provides verification helper methods. """

from utility.hash_util import hash_block, hash_string_256
from wallet import Wallet


class Verification:
    """ A helper class which offer verious static and class-based verification """
    @staticmethod  # not using anything from class
    def valid_proof(transactions, last_hash, proof):
        """ Validate a proof of work number and see if it solves the puzzle 

        Arguments:
            :transactions: The transactions of the block for which the proof of work working on.
            :last_hash: The previous block's hash which will be stored.
            :proof: The proof of work number we're testing.
        """
        # Create a string with the hash inputs
        guess = (str([tx.to_ordered_dict() for tx in transactions]) +
                 str(last_hash) + str(proof)).encode()
        # print(guess)
        guess_hash = hash_string_256(guess)
        # print(guess_hash)
        return guess_hash[0:2] == '00'

    @classmethod
    def verify_chain(cls, blockchain):
        """ Verify the current blockchain and return True if it is valid, Flase otherise. """
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index-1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        return True

    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        """ Verify a transaction by checking whether the sender has sufficient funds.

        Arguments:
            :transaction: The transaction that should be verified.
        """
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions])
