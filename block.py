from time import time
from utility.printable import Printable

class Block(Printable):
    def __init__(self, index, previous_hash, transactions, proof, timestamp=time()):
        self.previous_hash = previous_hash
        self.index = index
        self.proof = proof
        self.timestamp = timestamp
        self.transactions = transactions