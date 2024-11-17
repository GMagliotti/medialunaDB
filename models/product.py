from pydantic import BaseModel


class Product(BaseModel):
    product_id: int
    brand: str
    name: str
    description: str
    price: float
    stock: int

    class Config:
        orm_mode = True

