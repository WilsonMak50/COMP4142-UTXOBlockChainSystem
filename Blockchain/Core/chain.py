#This is the main program

import sys
sys.path.append('/Users/wilso/Desktop/COMP4142-Project/COMP4142-UTXOBlockChainSystem')
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
        prevTime=0
        difficutly=3
        self.addBlock(BlockIndex,prevHash,data,difficutly,prevTime)
        print("Created Genesis Block")

    def addBlock(self, BlockIndex, prevHash,data,difficulty, prevTime):
        timestamp= int(time.time())
        Transaction=f"This is Genesis block : {BlockIndex} "
        merkleRoot = hash_func(Transaction.encode()).hex()
        newhash = Block_Hash(BlockIndex,merkleRoot, timestamp,prevHash,difficulty,prevTime)
        mineTime=newhash.mine()
        self.write_on_db([
            Block(BlockIndex,newhash.__dict__,prevHash,data,mineTime).__dict__]
            )
        print("New Block Added")
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
            print(f"Current Block Height is {BlockIndex}")
            prevHash = lastBlock['hash']['curhash']
            self.addBlock(BlockIndex, prevHash,data,lastBlock['hash']['difficulty'],lastBlock['mineTime'])
            data = input('Please Enter some Data to create new block :')


if __name__ == "__main__":
    blockchain = Blockchain()
    blockchain.main()