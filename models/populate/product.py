class Product:
    def __init__(self, product_id, brand, name, description, price, stock):
        self.product_id = product_id
        self.brand = brand
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    def to_dict(self):
        return {
            "product_id": self.product_id,
            "brand": self.brand,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "stock": self.stock
        }