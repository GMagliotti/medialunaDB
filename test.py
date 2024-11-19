from services.client_service import ClientService
from services.invoice_service import InvoiceService
from services.product_service import ProductService
from models.populate.client import Client
from models.populate.product import Product
from persistence.invoice_repository import InvoiceRepository
from persistence.cassandra_connection import CassandraConnection
from persistence.mongo_connection import MongoConnection

def query1(client_service: ClientService):
    for client in client_service.get_clients():
        print(client.to_dict())

def query2(client_service: ClientService):
    for client in client_service.get_clients_by_name(first_name='Jacob', last_name='Cooper'):
        print(client.to_dict())

def query3(client_service: ClientService):
    for client in client_service.get_phones_with_client():
        print(client)

def query4(client_service: ClientService):
    for client in client_service.get_clients_with_invoices():
        print(client.to_dict())

def query5(client_service: ClientService):
    for client in client_service.get_clients_with_no_invoices():
        print(client.to_dict())

def query6(client_service: ClientService):
    for client in client_service.get_clients_with_invoice_count():
        print(client)

def query7(invoice_service: InvoiceService):
    for invoice in invoice_service.get_invoices_by_user_name_and_surname(first_name='Kai', last_name='Bullock'):
        print(invoice)

def query8(product_service: ProductService):
    for product in product_service.get_products_with_invoices():
        print(product)

def query9(invoice_service: InvoiceService):
    invoice_list = invoice_service.get_invoices_by_product_brand(brand='Ipsum')
    for invoice in invoice_list:
        for a in invoice:
            print(a['invoice'])
            print("---------------------------------------------------------------------------------------------------")

def query10(client_service: ClientService):
    for client in client_service.get_clients_with_total_expenses():
        print(client)

def query12(invoice_service: InvoiceService):
    invoice_service.create_view_no_invoice_products();

def query13(client_service: ClientService):
    client = Client(1986, 'Mario', 'Mario', 'Mushroom Kingdom', 't', [])
    client_service.add_client(client)
    client.first_name = 'Luigi'
    client_service.modify_client(client)
    client_service.delete_client_id(client.client_id)

def query14(product_service: ProductService):
    product = Product(1969, 'Dodge', 'Charger R/T', 'vroom vroom :)', 3575.0, 1)
    #product_service.add_product(product)
    product.name = 'Challenger R/T'
    product_service.modify_product(product)
    product_service.delete_product_by_id(product.product_id)

if __name__ == "__main__":
    cassandra_connection = CassandraConnection()
    mongo_connection = MongoConnection()
    client_service = ClientService(
        mongo_connection=mongo_connection, cassandra_connection=cassandra_connection
    )
    product_service = ProductService(mongo_connection, cassandra_connection)


    invoice_service = InvoiceService(mongo_connection, cassandra_connection)

    query8(product_service)

    """
    for client in client_service.get_clients_with_invoices():
        print(client.to_dict())

    for client in client_service.get_clients_with_invoice_count():
        print(client)

    for client in client_service.get_clients_with_total_expenses():
        print(client)
    clients_with_phones = client_service.get_phones_with_client()
    for c in clients_with_phones:
        print(c['_id'])
        print(c['client_id'])
        print(c['first_name'])
        print(c['last_name'])
        print(c['address'])
        print(c['active'])
        print(c['phone_numbers'])
    client_service.end()

    invoice_repo = InvoiceRepository(connection)
    for invoice in invoice_repo.get_invoices_ordered_by_date():
        print(invoice.date)

    connection.close()

    clients_m = []
    clients = client_service.get_clients_with_invoices(page=0, page_size=0)
    
    print(f'CLIENT WITH INVOICES: {len(list(clients))}')

    clients_2 = client_service.get_clients_with_no_invoices(page=0, page_size=0)
    print(f'CLIENT WITH NO INVOICES: {len(list(clients))}')
    for c in clients_2:
        print(f'{c.client_id}\n')
    
    clients = client_service.get_clients(page=0, page_size=0)
    print(f'TOTAL CLIENTS: {len(list(clients))}')

    clients = client_service.get_clients_with_invoice_count(page=0, page_size=0)
    
    client_service.end()
    
    print(len(clients))
    print(f'{list(map(lambda a: a['invoice_count'], clients))}')
    print(clients[57])
    print(clients[61])
    clients = list(client_service.get_clients_with_total_expenses(page=0, page_size=0))

    for c in clients:
        print(c['client'].first_name)
        print(c['client'].last_name)
        print(c['expenses'])
    
    invoices = invoice_service.get_invoices_by_product_brand(brand="Ipsum", page=0, page_size=0)
    print(invoices)
    """
    """
    * Q1  RUNS
    * Q2  RUNS
    * Q3  RUNS
    * Q4  RUNS
    * Q5  RUNS
    * Q6  RUNS
    * Q7  RUNS
    * Q8  RUNS
    * Q9  RUNS
    * Q10 RUNS
    * Q11 ?
    * Q12 ?
    * Q13 WORKS
    * Q14 WORKS
    """

