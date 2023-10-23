import hashlib

def hash_func(s):
    #hash function to hash twice
    return hashlib.sha256(hashlib.sha256(s).digest()).digest()