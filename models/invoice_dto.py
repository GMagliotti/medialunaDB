from pydantic import BaseModel
from typing import List
from models.invoice_detail_dto import InvoiceDetailDTO
from datetime import datetime, timedelta, date


class InvoiceDTO(BaseModel):
    invoice_id: int
    date: str
    total_with_tax: float
    tax: float
    #client_id: int
    invoice_detail: List[InvoiceDetailDTO]

    @staticmethod
    def from_model(invoice_model, details_model_list):
        return InvoiceDTO(
            invoice_id=invoice_model.invoice_id,
            date=str(invoice_model.date),
            total_with_tax=invoice_model.total_with_tax,
            tax=invoice_model.tax,
            invoice_detail=[InvoiceDetailDTO.from_model(d) for d in details_model_list],
        )

