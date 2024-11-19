from pydantic import BaseModel


class InvoiceDetailDTO(BaseModel):
    product_id: int
    item_number: float
    amount: float

    @staticmethod
    def from_model(model):
        return InvoiceDetailDTO(
            product_id=model.product_id,
            item_number=model.item_number,
            amount=model.amount,
        )