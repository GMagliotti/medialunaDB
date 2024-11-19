from persistence.product_repository import ProductRepository
from persistence.invoice_repository import InvoiceRepository
from models.populate.product import Product


class ProductService:
    def __init__(self, mongo_connection, cassandra_connection):
        self.product_repository = ProductRepository(mongo_connection)
        self.invoice_repository = InvoiceRepository(cassandra_connection)

    def create_view_no_invoice_products(self):
        product_ids = list(self.invoice_repository.get_invoices_product_ids())
        return self.product_repository.create_view_no_invoice_products(product_ids)

    def get_products(self):
        return self.product_repository.get_products()

    def get_products_with_no_invoice(self):
        product_ids = list(self.invoice_repository.get_invoices_product_ids())
        return self.product_repository.get_products_with_no_invoice()

    def get_products_with_invoices(self):
        product_ids = list(self.invoice_repository.get_invoices_product_ids())
        return self.product_repository.get_products_with_invoices(list(product_ids))

    def get_product_ids_with_invoices(self):
        return list(frozenset(self.invoice_repository.get_invoices_product_ids()))

    def add_product(self, product: Product):
        self.product_repository.insert_one(product)

    def modify_product(self, product: Product):
        self.product_repository.update_one(product)

    def delete_product(self, product: Product):
        self.product_repository.delete_one(product)

    def delete_product_by_id(self, product_id: int):
        self.product_repository.delete_one_by_id(product_id)

