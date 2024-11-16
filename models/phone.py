from pydantic import BaseModel


class Phone(BaseModel):
    area_code: int
    phone_number: int
    type: str
    client_id: int
        