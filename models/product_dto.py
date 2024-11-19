from pydantic import BaseModel

class ProductDTO(BaseModel):
    product_id: int
    brand: str
    name: str
    description: str
    price: float
    stock: int

    @staticmethod
    def from_model(product_model):
        return ProductDTO(
            product_id=product_model.product_id,
            brand=product_model.brand,
            name=product_model.name,
            description=product_model.description,
            price=product_model.price,
            stock=product_model.stock
        )

    @staticmethod
    def from_dict(product_dict: dict):
        return ProductDTO(
            product_id=product_dict.get('product_id'),
            brand=product_dict.get('brand'),
            name=product_dict.get('name'),
            description=product_dict.get('description'),
            price=product_dict.get('price'),
            stock=product_dict.get('stock')
        )
