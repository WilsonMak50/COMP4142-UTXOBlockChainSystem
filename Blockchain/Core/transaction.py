from Blockchain.Core.script import Script
from Blockchain.Core.util.util import (
    int_to_little_endian,
    bytes_needed,
    decode_base58,
    little_endian_to_int,
    encode_varint,
    hash_func,
    read_varint
)



ZERO_HASH = b"\0" * 32
REWARD = 50

PRIVATE_KEY='6574444187975193754546146859541371601379842442519722510363305547219679102529'
MINER_ADDRESS='1DqeqQQeVDs6rNRr46R4n6YwanpxGMRn9X'
SIGNHASH_ALL=1
class CoinbaseTx:
    def __init__(self, BlockHeight):
        self.BlockHeightInLittleEndian = int_to_little_endian(
            BlockHeight, bytes_needed(BlockHeight)
        )

    def CoinbaseTransaction(self):
        prev_tx = ZERO_HASH
        prev_index = 0xFFFFFFFF
        tx_ins = []
        tx_ins.append(Tx_In(prev_tx, prev_index))
        tx_ins[0].script_sig.cmds.append(self.BlockHeightInLittleEndian)
       

        tx_outs = []
        target_amount = REWARD * 100000000
        target_h160 = decode_base58(MINER_ADDRESS)
        target_script = Script.p2pkh_script(target_h160)
        tx_outs.append(Tx_Out(amount=target_amount, script_pubkey=target_script))
        coinBaseTx = Tx(tx_ins, tx_outs, 0)
        coinBaseTx.TxId = coinBaseTx.id()
        return coinBaseTx
        

class Tx:
    def __init__(self, tx_ins, tx_outs, tx_time):
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.tx_time = tx_time
    
    def id(self):
        return self.hash().hex()
    def hash(self):
        return hash_func(self.serialize())[::-1]

    def serialize(self):
        
        result = encode_varint(len(self.tx_ins))

        for tx_in in self.tx_ins:
            result += tx_in.serialize()

        result += encode_varint(len(self.tx_outs))

        for tx_out in self.tx_outs:
            result += tx_out.serialize()

        result += int_to_little_endian(self.tx_time, 4)
        return result
    
    def signature_hash(self, input_index, script_pubkey):
        s = int_to_little_endian(self.version, 4)
        s += encode_varint(len(self.tx_ins))

        for i, tx_in in enumerate(self.tx_ins):
            if i == input_index:
                s += Tx_In(tx_in.prev_tx, tx_in.prev_index, script_pubkey).serialize()
            else:
                s += Tx_In(tx_in.prev_tx, tx_in.prev_index).serialize()

        s += encode_varint(len(self.tx_outs))

        for tx_out in self.tx_outs:
            s += tx_out.serialize()

        s += int_to_little_endian(self.locktime, 4)
        s += int_to_little_endian(SIGNHASH_ALL, 4)
        h256 = hash_func(s)
        return int.from_bytes(h256, "big")
    def sign_input(self, input_index, private_key, script_pubkey):
        z = self.signature_hash(input_index, script_pubkey)
        der = private_key.sign(z).der()
        sig = der + SIGNHASH_ALL.to_bytes(1, "big")
        sec = private_key.point.sec()
        self.tx_ins[input_index].script_sig = Script([sig, sec])

    def verify_input(self, input_index, script_pubkey):
        tx_in = self.tx_ins[input_index]
        z = self.signature_hash(input_index, script_pubkey)
        combined = tx_in.script_sig + script_pubkey
        return combined.evaluate(z)

    
    
    def is_coinbase(self):
        """
        # Check that there us exactly 1 input
        # grab the first input and check if the prev_tx is b'\x00' * 32
        # check that the first input prev_index is 0xffffffff
        """

        if len(self.tx_ins) != 1:
            return False

        first_input = self.tx_ins[0]

        if first_input.prev_tx != b"\x00" * 32:
            return False

        if first_input.prev_index != 0xFFFFFFFF:
            return False

        return True
    
    def to_dict(self):
        """
        Convert Transaction
         # Convert prev_tx Hash in hex from bytes
         # Convert Blockheight in hex which is stored in Script signature
        """
        if self.is_coinbase():
            self.tx_ins[0].prev_tx =self.tx_ins[0].prev_tx.hex()
            self.tx_ins[0].script_sig.cmds[0]=little_endian_to_int(self.tx_ins[0].script_sig.cmds[0])
            self.tx_ins[0].script_sig= self.tx_ins[0].script_sig.__dict__

        self.tx_ins[0] = self.tx_ins[0].__dict__

        self.tx_outs[0].script_pubkey.cmds[2]=self.tx_outs[0].script_pubkey.cmds[2].hex()
        self.tx_outs[0].script_pubkey = self.tx_outs[0].script_pubkey.__dict__
        self.tx_outs[0] = self.tx_outs[0].__dict__

        return self.__dict__
    
    
    @classmethod
    def to_obj(cls, item):
        TxInList = []
        TxOutList = []
        cmds = []

        """ Convert Transaction Input to the object """
        for tx_in in item['tx_ins']:
            for cmd in tx_in['script_sig']['cmds']:
               
                if tx_in['prev_tx'] == "0000000000000000000000000000000000000000000000000000000000000000":
                    cmds.append(int_to_little_endian(int(cmd), bytes_needed(int(cmd))))
                else:
                    if type(cmd) == int:
                        cmds.append(cmd)
                    else:
                        cmds.append(bytes.fromhex(cmd))
            TxInList.append(Tx_In(bytes.fromhex(tx_in['prev_tx']),tx_in['prev_index'],Script(cmds)))   

        
        """" Convert Transaction output to Object """
        cmdsout = []
        for tx_out in item['tx_outs']:
            for cmd in tx_out['script_pubkey']['cmds']:
                if type(cmd) == int:
                    cmdsout.append(cmd)
                else:
                    cmdsout.append(bytes.fromhex(cmd))
                    
            TxOutList.append(Tx_Out(tx_out['amount'],Script(cmdsout)))
            cmdsout= []
        
        return cls(1, TxInList, TxOutList, 0)
                


    


class Tx_In:
    def __init__(self, prev_tx, prev_index, script_sig =None, sequence=0xFFFFFFFF ):
        self.prev_tx=prev_tx
        self.prev_index=prev_index
        if script_sig is None:
            self.script_sig=Script()
        else:
            self.script_sig=script_sig 
        script_sig=script_sig
        self.sequence = sequence

    def serialize(self):
        result = self.prev_tx[::-1]
        result += int_to_little_endian(self.prev_index, 4)
        result += self.script_sig.serialize()
        result += int_to_little_endian(self.sequence, 4)
        return result

class Tx_Out:
    def __init__(self, amount, script_pubkey):
        self.amount= amount
        self.script_pubkey=script_pubkey

    def serialize(self):
        result = int_to_little_endian(self.amount, 8)
        result += self.script_pubkey.serialize()
        return result

        