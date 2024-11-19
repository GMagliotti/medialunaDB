from pydantic import BaseModel
from models.phone import Phone

class ClientPhonesResponse(BaseModel):
    client_id: int
    phones: list[Phone]

    class Config:
        orm_mode = True
