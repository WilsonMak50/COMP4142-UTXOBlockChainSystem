import time
from Blockchain.Core.util.util import hash_func
class Block_Hash:
    def __init__(self, index, root, timestamp,prevHash,difficulty,prevTime):
        self.index = index
        self.root = root
        self.timestamp = timestamp
        self.prevHash = prevHash
        self.difficulty = difficulty
        self.nonce=0
        self.curhash = ''
        self.prevTime= prevTime
    
    def mine(self):
        if self.prevTime<=10:
            self.difficulty=self.difficulty+1
        else:
            self.difficulty=self.difficulty-1
            
        start_time = time.time()
        while (self.curhash[0:self.difficulty])!='0'*self.difficulty:
            self.curhash=hash_func((str(self.index)+ str(self.root)+str(self.timestamp)+
                                 self.prevHash+str(self.difficulty)+str(self.nonce)).encode()).hex()
            self.nonce +=1
            print(f"Mining: {self.nonce}",end='\r')
        elapsed_time = time.time() - start_time
        return elapsed_time
