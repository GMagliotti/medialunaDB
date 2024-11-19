from pydantic import BaseModel

class InvoiceDetailDTO(BaseModel):
    product_id: int
    item_number: float
    amount: float

    @staticmethod
    def from_model(model):
        pass