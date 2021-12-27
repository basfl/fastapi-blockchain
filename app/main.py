import fastapi as _fastapi
from . import blockchain as _blockchain

from . import schemas


blockchain = _blockchain.BlockChain()
app = _fastapi.FastAPI()


@app.get("/")
async def root():
    return {"message": "welcome to my blockchain api"}


# endpoint to mine a block
@app.post("/mine_block/")
def mine_block(request: schemas.Request):
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    block = blockchain.mine_block(data=request.data)

    return block


# endpoint to return the blockchain
@app.get("/blockchain/")
def get_blockchain():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    chain = blockchain.chain
    return chain

# endpoint to see if the chain is valid


@app.get("/validate/")
def is_blockchain_valid():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")
    return blockchain.is_chain_valid()

# endpoint to return the last block


@app.get("/blockchain/last/")
def previous_block():
    if not blockchain.is_chain_valid():
        return _fastapi.HTTPException(status_code=400, detail="The blockchain is invalid")

    return blockchain.get_previous_block()
