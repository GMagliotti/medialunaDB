class Product:
    def __init__(self, product_id: int, brand: str, name: str, description: str, price: float, stock: int):
        self.product_id = product_id
        self.brand = brand
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock