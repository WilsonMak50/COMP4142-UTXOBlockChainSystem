class Block:
    """
    Block is a storage containter that stores transactions
    """

    def __init__(self, Index, hash, prevHash, data,mineTime):
        self.Index = Index
        self.hash= hash
        self.prevHash = prevHash
        self.data = data
        self.mineTime = mineTime