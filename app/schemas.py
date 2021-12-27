from pydantic import BaseModel


class Request(BaseModel):
    data: str


class Response(BaseModel):
    index: int
    data: str
    proof: int
    previous_hash: str
    timestamp: str
