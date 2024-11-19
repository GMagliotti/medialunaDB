from services.client_service import ClientService
from persistence.invoice_repository import InvoiceRepository
from persistence.cassandra_connection import CassandraConnection
from persistence.mongo_connection import MongoConnection

if __name__ == "__main__":
    cassandra_connection = CassandraConnection()
    mongo_connection = MongoConnection()
    client_service = ClientService(
        mongo_connection=mongo_connection, cassandra_connection=cassandra_connection
    )
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
    """
    clients = list(client_service.get_clients_with_total_expenses(page=0, page_size=0))

    for c in clients:
        print(c['client'].first_name)
        print(c['client'].last_name)
        print(c['expenses'])