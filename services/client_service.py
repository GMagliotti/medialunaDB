from typing import List
from models.populate.client import Client
from models.populate.phone import Phone
from models.client import Client as ClientDTO
from models.phone import Phone as PhoneDTO
from fastapi import HTTPException
from persistence.client_repository import ClientRepository
from persistence.invoice_repository import InvoiceRepository
from persistence.mongo_connection import MongoConnection
from persistence.cassandra_connection import CassandraConnection


class ClientService:
    def __init__(
        self,
        mongo_connection=MongoConnection(),
        cassandra_connection=CassandraConnection(),
    ):
        self.client_repository = ClientRepository(mongo_connection)
        self.invoice_repository = InvoiceRepository(cassandra_connection)

    def get_clients(self, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        return self.client_repository.get_clients(skip=skip, limit=limit)
        
    def get_clients_by_name(
        self, first_name: str, last_name: str, page: int = 0, pageSize: int = 0
    ):
        skip = page * pageSize
        limit = pageSize
        return self.client_repository.get_clients_by_name(
            first_name, last_name, skip=int(skip), limit=int(limit)
        )

    def get_phones_with_client(self, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        return self.client_repository.get_phones_with_client(skip=skip, limit=limit)

    def get_clients_with_invoices(self, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        client_ids = self.invoice_repository.get_invoices_client_ids()
        return self.client_repository.get_clients(
            filter={"client_id": {"$in": list(client_ids)}}, skip=int(skip), limit=int(limit)
        )

    def get_clients_with_invoice_count(self, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        clients = self.client_repository.get_clients(skip=skip, limit=limit)
        clients_with_invoice_count = []
        for c in clients:
            clients_with_invoice_count.append(
                {
                    "client": c,
                    "invoice_count": self.invoice_repository.get_count_by_client(client_id=c.client_id),
                }
            )
        return clients_with_invoice_count

    def get_clients_with_total_expenses(self, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        clients = self.client_repository.get_clients(skip=skip, limit=limit)
        clients_with_expenses = []
        for c in clients:
            clients_with_expenses.append(
                {
                    "client": c,
                    "expenses": self.invoice_repository.get_client_total_expenses(c.client_id),
                }
            )
        return clients_with_expenses

    def get_clients_with_no_invoices(self, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        client_ids = self.invoice_repository.get_invoices_client_ids()
        return self.client_repository.get_clients(
            {"client_id": {"$nin": list(client_ids)}}, skip, limit
        )

    def add_client(self, client: Client):
        self.client_repository.insert_one(client)

    def add_clients(self, clients: list[Client]):
        self.client_repository.insert_many(clients)

    def edit_client(self, client: Client):
        self.client_repository.update_one(client)

    def delete_client(self, client: Client):
        self.client_repository.delete_one(client)

    def modify_client(self, client: Client):
        self.client_repository.update_one(client)

    def delete_client(self, client: Client):
        self.client_repository.delete_one(client)

    def delete_client_id(self, client_id: int):
        self.client_repository.delete_one(client_id)

    def end(self):
        self.invoice_repository.close()

    # def __init__(self, mongo_client: MongoConnection):
    #     self.db = mongo_client.get_db()
    #     self.collection = self.db["clients"]

    # def get_clients(self) -> List[Client]:
    #     clients = []
    #     for client in self.collection.find():
    #         clients.append(Client(**client))
    #     return clients

    # def get_client_by_name(self, first_name: str, last_name: str) -> List[Phone]:
    #     client_data = self.collection.find_one({"first_name": first_name, "last_name": last_name})
    #     if not client_data:
    #         raise HTTPException(status_code=404, detail="Client not found")
    #     phones = []
    #     for phone in client_data.get("phone_list", []):
    #         phones.append(Phone(**phone))
    #     return phones
