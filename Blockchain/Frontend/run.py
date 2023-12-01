from flask import Flask, render_template, request
from Blockchain.Core.Client.sendCoin import SendCoin
from Blockchain.Core.transaction import Tx
app=Flask(__name__)
@app.route('/',methods= ["GET","POST"])
def wallet():
    message=''
    if request.method == "POST":
        FromAddress = request.form.get("fromAddress")
        ToAddress = request.form.get("toAddress")
        Amount = request.form.get("Amount", type=int)
        sendCoin = SendCoin(FromAddress, ToAddress, Amount,UTXOS)
        
        TxObj =sendCoin.prepareTransaction()
        scriptPubKey=sendCoin.scriptPubKey(FromAddress)
        verified=True

        if not TxObj:
            message ="Invalid Transaction"
        
        if isinstance(TxObj, Tx):
            for index, yx in enumerate(TxObj.tx_input):
                if not TxObj.verify_input(index,scriptPubKey):
                    verified=False 
            if verified:
                MEMPOOL[TxObj.TxId]=TxObj
                message = "Transaction added in memory Pool"

    return render_template('wallet.html',message=message)
def main(utxos, MemPool):
    global UTXOS
    global MEMPOOL
    UTXOS = utxos
    MEMPOOL = MemPool
    app.run()