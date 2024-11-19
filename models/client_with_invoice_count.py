from pydantic import BaseModel
from typing import List
from models.phone import Phone


class ClientWithInvoiceCount(BaseModel):
    client_id: int
    first_name: str
    last_name: str
    address: str
    active: int
    phones: List[Phone]
    invoice_count: int

    @staticmethod
    def from_model(model):
        return ClientWithInvoiceCount(
            client_id=model['client'].client_id,
            first_name=model['client'].first_name,
            last_name=model['client'].last_name,
            address=model['client'].address,
            active=model['client'].active,
            phones=[Phone.from_model(phone) for phone in model['client'].phone_list],
            invoice_count=model['invoice_count']
        )

    class Config:
        orm_mode = True
    

