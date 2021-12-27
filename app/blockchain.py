import datetime as _dt
import hashlib as _hashlib
import json as _json


class BlockChain:
    def __init__(self) -> None:
        self.chain = list()
        genesis_block = self._create_block(
            data="this is genesis block", proof=1, previous_hash="0", index=1)
        self.chain.append(genesis_block)
        

    def mine_block(self, data: str) -> dict:
        previous_block = self.get_previous_block()
        previous_proof = previous_block["proof"]
        index = len(self.chain) + 1
        proof = self._proof_of_work(
            previous_proof=previous_proof, index=index, data=data)
        previous_hash = self._hash(block=previous_block)
        block = self._create_block(
            data=data, proof=proof, previous_hash=previous_hash, index=index
        )

        self.chain.append(block)
        return block

    def _proof_of_work(self, previous_proof: str, index: int, data: str) -> int:
        new_proof = 1
        check_proof = False
        while not check_proof:
            _to_digest = self._to_digest(
                new_proof=new_proof, previous_proof=previous_proof, index=index, data=data)
            hash_value = _hashlib.sha256(_to_digest).hexdigest()
            if hash_value[:4] == "0000":
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def _to_digest(
        self, new_proof: int, previous_proof: int, index: int, data: str
    ) -> bytes:
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + data
        # It returns an utf-8 encoded version of the string
        return to_digest.encode()

    def _hash(self, block: dict) -> str:
        """
        Hash a block and return the crytographic hash of the block
        """
        encoded_block = _json.dumps(block, sort_keys=True).encode()

        return _hashlib.sha256(encoded_block).hexdigest()

    def get_previous_block(self) -> dict:
        return self.chain[-1]

    def _create_block(self, data: str, proof: int, previous_hash: str, index: int) -> dict:
        block = {
            "index": index,
            "timestamp": str(_dt.datetime.now()),
            "data": data,
            "proof": proof,
            "previous_hash": previous_hash,
        }
        return block

    def is_chain_valid(self) -> bool:
        previous_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            block = self.chain[block_index]
            # Check if the previous hash of the current block is the same as the hash of it's previous block
            if block["previous_hash"] != self._hash(previous_block):
                return False

            previous_proof = previous_block["proof"]
            index, data, proof = block["index"], block["data"], block["proof"]
            hash_operation = _hashlib.sha256(
                self._to_digest(
                    new_proof=proof,
                    previous_proof=previous_proof,
                    index=index,
                    data=data,
                )
            ).hexdigest()

            if hash_operation[:4] != "0000":
                return False

            previous_block = block
            block_index += 1

        return True
