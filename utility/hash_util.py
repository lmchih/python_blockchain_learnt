""" Provides cryptographical alogorithms. """


import hashlib as hl
import json

""" Limiting exports """
# __all__ = ['hash_string_256', 'hash_block']


def hash_string_256(string):
    return hl.sha256(string).hexdigest()


def hash_block(block):
    """ Hashes a block and returns a string representation of it. 

    Arguments:
        :block: The block that should be hashed.
    """
    # hashable_block = block.__dict__.copy()
    # print(hashable_block)
    hashable_block = block.__dict__.copy()
    print(hashable_block)
    hashable_block['transactions'] = [tx.to_ordered_dict()
                                      for tx in hashable_block['transactions']]
    # sha256 only takes string as input
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())
