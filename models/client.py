from pydantic import BaseModel
from typing import List
from models.phone import Phone


class Client(BaseModel):
    client_id: int
    first_name: str
    last_name: str
    address: str
    active: int
    phone: List[Phone]

    class Config:
        orm_mode = True
