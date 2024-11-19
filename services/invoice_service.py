from persistence.product_repository import ProductRepository
from persistence.invoice_repository import InvoiceRepository
from persistence.client_repository import ClientRepository

class InvoiceService:
    def __init__(self, mongo_connection, cassandra_connection):
        self.client_repository = ClientRepository(mongo_connection)
        self.invoice_repository = InvoiceRepository(cassandra_connection)
    
    def get_invoices_by_user_name_and_surname(self, first_name: str, last_name: str, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        client_data = self.client_repository.get_clients({"first_name": first_name, "last_name": last_name}, skip=skip, limit=limit)[0]
        invoices = self.invoice_repository.get_invoices_by_client_id(client_data['client_id'])
        # TODO -> Hay que transformarlo al DTO para que devuelva bien en FastAPI
        return invoices