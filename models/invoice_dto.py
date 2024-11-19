from pydantic import BaseModel
from typing import List
from invoice_detail_dto import InvoiceDetailDTO
from datetime import date

class InvoiceDTO(BaseModel):
    invoice_id: int
    date: date
    amount_with_tax: float
    tax: float
    client_id: int
    invoice_detail: List[InvoiceDetailDTO]

    @staticmethod
    def from_model(model):
        pass