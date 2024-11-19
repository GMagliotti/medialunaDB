from models.product import Product
from persistence.mongo_connection import MongoConnection

class ProductRepository:
    _COLLECTION_NAME = 'products'

    def __init__(self, host='localhost', port=27017, database='db'):
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

    def update_one(self, product: Product):
        self.mongo.get_collection(self._COLLECTION_NAME).update_one(filter={'product_id': product.product_id}, update={'$set': self._product_to_dict(product)})

    def delete_one(self, product: Product):
        self.mongo.get_collection(self._COLLECTION_NAME).delete_one({'product_id': product.product_id})

    def create_view_no_invoice_products(self, product_ids: list):
        view_name = "no_invoice_products"
        self.mongo.drop_view(view_name)
        view_on_name = "products"
        pipeline = [{'$match': {'product_id': {'$nin': product_ids}}}]
        self.mongo.create_view(view_name, view_on_name, pipeline)
    
    def get_products_with_no_invoice(self):
        view_name = "no_invoice_products"
        return self.mongo.get_collection(view_name).find()
    
    def get_products_with_invoices(self, product_ids: list[int]):
        return self._dict_to_product(
            self.mongo.get_collection(self._COLLECTION_NAME).find({'product_id': { "$in": product_ids}})
            );


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
