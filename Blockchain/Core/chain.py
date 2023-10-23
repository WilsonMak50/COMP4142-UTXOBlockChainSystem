import sys
sys.path.append('/Users/wilso/Desktop/COMP4142-Project')
import time
from Blockchain.Core.block_hash import Block_Hash
from Blockchain.Core.block import Block
from Blockchain.Core.util.util import hash_func
from Blockchain.Core.Database.database import BlockchainDB
import json

class Blockchain:
    
    def write_on_db(self,block):
        blockchainDB=BlockchainDB()
        blockchainDB.write(block)

    def fetch_last_block(self):
        blockchainDB=BlockchainDB()
        return blockchainDB.lastBlock()
    
    def GenesisBlock(self):
        BlockIndex=0
        prevHash= '0'*64
        data = "COMP4142"
        self.addBlock(BlockIndex,prevHash,data)

    def addBlock(self, BlockIndex, prevHash,data):
        timestamp= int(time.time())
        Transaction=f"This is Genesis block : {BlockIndex} "
        merkleRoot = hash_func(Transaction.encode()).hex()
        newhash = Block_Hash(BlockIndex,merkleRoot, timestamp,prevHash, 4 )
        print("New Block Added")
        newhash.mine()
        self.write_on_db([
            Block(BlockIndex,newhash.__dict__,prevHash,data).__dict__]
            )
        #print(json.dumps(self.chain, indent=4))

    def main(self):
       lastBlock = self.fetch_last_block()
       if lastBlock is None:
            self.GenesisBlock()
       else: 
           BlockIndex=lastBlock["Index"]
           print(f"Current Block Index {BlockIndex}")
       data = input('Please Enter some Data to create new block :')
       while data!='':
            lastBlock= self.fetch_last_block()
            BlockIndex = lastBlock["Index"]+1
            print(f"Current Block Height is is {BlockIndex}")
            prevHash = lastBlock['hash']['curhash']
            self.addBlock(BlockIndex, prevHash,data)
            data = input('Please Enter some Data to create new block :')


if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.main()