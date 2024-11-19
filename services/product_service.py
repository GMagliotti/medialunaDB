from persistence.product_repository import ProductRepository
from persistence.invoice_repository import InvoiceRepository

class ProductService:
    def __init__(self, mongo_connection, cassandra_connection):
        self.product_repository = ProductRepository(mongo_connection)
        self.invoice_repository = InvoiceRepository(cassandra_connection)
    
    def create_view_no_invoice_products(self):
        product_ids = list(self.invoice_repository.get_invoices_product_ids())
        return self.product_repository.create_view_no_invoice_products(product_ids)

    def get_products_with_no_invoice(self):
        product_ids = list(self.invoice_repository.get_invoices_product_ids())
        return self.product_repository.get_products_with_no_invoice()

    def get_products_with_invoices(self):
        product_ids = list(self.invoice_repository.get_invoices_product_ids())
        return self.product_repository.get_products_with_invoices(list(product_ids))