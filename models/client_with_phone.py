from pydantic import BaseModel
from models.phone import Phone

class PhoneWithClient(BaseModel):
    phone_number: int
    area_code: int
    type: str
    client_id: int
    first_name: str
    last_name: str
    address: str
    active: int

    class Config:
        orm_mode = True