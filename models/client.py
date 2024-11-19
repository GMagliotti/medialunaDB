from pydantic import BaseModel
from typing import List
from models.phone import Phone


class Client(BaseModel):
    client_id: int
    first_name: str
    last_name: str
    address: str
    active: int
    phones: List[Phone]

    @staticmethod
    def from_model(model):
        return Client(
            client_id=model.client_id,
            first_name=model.first_name,
            last_name=model.last_name,
            address=model.address,
            active=model.active,
            phones=[Phone.from_model(phone) for phone in model.phone_list],
        )

    class Config:
        orm_mode = True
    

