from persistence.product_repository import ProductRepository
from persistence.invoice_repository import InvoiceRepository
from persistence.client_repository import ClientRepository
from persistence.product_repository import ProductRepository


class InvoiceService:
    def __init__(self, mongo_connection, cassandra_connection):
        self.client_repository = ClientRepository(mongo_connection)
        self.product_repository = ProductRepository(mongo_connection)
        self.invoice_repository = InvoiceRepository(cassandra_connection)

    def get_invoices_by_user_name_and_surname(self, first_name: str, last_name: str, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        clients = list(self.client_repository.get_clients({"first_name": first_name, "last_name": last_name}, skip=skip, limit=limit))
        client_data = clients[0]
        client_id = client_data.client_id
        invoices = self.invoice_repository.get_invoices_by_client_id(client_id)
        return invoices


    def get_invoices_by_product_brand(self, brand: str, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        products = list(self.product_repository.get_products_by_product_brand(brand, skip, limit))
        product_ids = map(lambda p: p.product_id, products)
        invoices = []

        for p in product_ids:
            invoices.extend(list(self.invoice_repository.get_invoices_by_product_id(p)))

        return invoices

    def get_invoice_ordered_by_date(self):
        return self.invoice_repository.get_invoices_ordered_by_date()
