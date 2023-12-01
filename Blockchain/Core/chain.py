#This is the main program

import sys
import configparser
sys.path.append('/Users/wilso/Desktop/COMP4142-Project/COMP4142-UTXOBlockChainSystem')
import time
from Blockchain.Core.block_hash import Block_Hash
from Blockchain.Core.block import Block
from Blockchain.Core.util.util import hash_func
from Blockchain.Core.Database.database import BlockchainDB
import json
from Blockchain.Core.Network.Net_sync import Net_sync
from multiprocessing import Process, Manager
from Blockchain.Core.transaction import CoinbaseTx
from Blockchain.Frontend.run import main
class Blockchain:
    def __init__(self,utxos,MemPool):
        self.utxos=utxos
        self.MemPool= MemPool
    
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

    def store_uxtos_in_cache(self,transaction):
        self.utxos[transaction.TxId] = transaction
 

    def addBlock(self, BlockIndex, prevHash,data,difficulty, prevTime):
        timestamp= int(time.time())
        coinbase_Ins = CoinbaseTx(BlockIndex)
        conbaseTx=coinbase_Ins.CoinbaseTransaction()
        merkleRoot = conbaseTx.TxId
        newhash = Block_Hash(BlockIndex,merkleRoot, timestamp,prevHash,difficulty,prevTime)
        mineTime=newhash.mine()
        self.store_uxtos_in_cache(conbaseTx)
        self.write_on_db([
            Block(BlockIndex,newhash.__dict__,prevHash,conbaseTx.to_dict(),mineTime).__dict__]
            )
        print("New Block Added")
        #print(json.dumps(self.chain, indent=4))

    def main(self):
       lastBlock = self.fetch_last_block()
       if lastBlock is None:
            self.GenesisBlock()
       
       while True:
            lastBlock= self.fetch_last_block()
            BlockIndex = lastBlock["Index"]+1
            
            prevHash = lastBlock['hash']['curhash']
            self.addBlock(BlockIndex, prevHash,'EMPTY-TEST',lastBlock['hash']['difficulty'],lastBlock['mineTime'])
           


if __name__ == "__main__":
    with Manager() as manager:
        utxos=manager.dict()
        MemPool=manager.dict()
        webapp=Process(target = main, args=(utxos,MemPool))
        webapp.start()

        blockchain = Blockchain(utxos, MemPool)
        blockchain.main()

"""
    config = configparser.ConfigParser() 
    config.read('config.ini')
    localHost = config['DEFAULT']['host']
    localHostPort = int(config['MINER']['port']) 
    webport = int(config['Webhost']['port'])
"""
    

    #Network
    #sync = Net_sync(localHost,localHostPort)
    #startServer = Process(target = sync.spinUPTheServer)
    #startServer.start()
    