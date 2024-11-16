from pydantic import Field
from beanie import Document


class Product(Document):
    product_id: int = Field(..., unique=True)
    brand: str
    name: str
    description: str
    price: float
    stock: int
