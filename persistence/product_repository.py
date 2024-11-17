from models.product import Product
from mongo_connection import MongoConnection

class ProductRepository:
    _COLLECTION_NAME = 'products'

    def __init__(self, host, port, database):
        # TODO receive the database connection as a parameter
        self.mongo: MongoConnection = MongoConnection();
    
    def get_products(self):
        cursor = self.mongo.get_collection(self._COLLECTION_NAME).find(filter={}, batch_size=100);
        with cursor:
            for product in cursor:
                yield self._dict_to_product(product)

    def get_product(self, product_id: int) -> Product:
        return self._dict_to_product(
            self.mongo.get_collection(self._COLLECTION_NAME).find_one({'product_id': product_id})
            );


    def insert_one(self, product: Product):
        return self.mongo.get_collection(self._COLLECTION_NAME).insert_one(self._product_to_dict(product))
    
    def insert_many(self, products: list[Product]):
        collection = self.mongo.get_collection(self._COLLECTION_NAME)
        product_docs = (self._product_to_dict(product) for product in products)
        collection.insert_many(product_docs)

    def _product_to_dict(self, product: Product) -> dict:
        return {
            'product_id': product.product_id,
            'brand': product.brand,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'stock': product.stock
        }
    
    def _dict_to_product(self, product_dict) -> Product:
        return Product(
            product_dict['product_id'],
            product_dict['brand'],
            product_dict['name'],
            product_dict['description'],
            product_dict['price'],
            product_dict['stock']
        )