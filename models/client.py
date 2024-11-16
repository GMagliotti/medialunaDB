from pydantic import Field
from models.phone import Phone
from beanie import Document
from typing import List


class Client(Document):
    client_id: int = Field(..., unique=True)
    first_name: str
    last_name: str
    address: str
    active: int
    phone: List[Phone]
