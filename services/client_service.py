from typing import List
from models.populate.client import Client
from models.populate.phone import Phone
from fastapi import HTTPException
from persistence.client_repository import ClientRepository


class ClientService:
    def __init__(self, host: str = 'localhost', port: int = 27017, database: str = 'db'):
        self.client_repository = ClientRepository(host = host, port = port, database = database);

    def get_clients(self, page: int = 0, page_size:int  = 0):
        skip = page * page_size
        limit = page_size
        return self.client_repository.get_clients(skip=skip, limit=limit)

    def get_clients_by_name(self, first_name: str, last_name: str, page: int = 0, pageSize: int = 0):
        skip = page * pageSize
        limit = pageSize
        return self.client_repository.get_clients_by_name(first_name, last_name, skip=skip, limit=limit)

    def get_phones_with_client(self, page: int = 0, page_size: int = 0):
        skip = page * page_size
        limit = page_size
        return self.client_repository.get_phones_with_client(skip=skip, limit=limit)


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