from typing import List
from models.client import Client
from models.phone import Phone
from fastapi import HTTPException
from persistence.mongo_connection import MongoConnection


class ClientService:
    def __init__(self, mongo_client: MongoConnection):
        self.db = mongo_client.get_db()
        self.collection = self.db["clients"]

    def get_clients(self) -> List[Client]:
        clients = []
        for client in self.collection.find():
            clients.append(Client(**client))
        return clients

    def get_client_by_name(self, first_name: str, last_name: str) -> List[Phone]:
        client_data = self.collection.find_one({"first_name": first_name, "last_name": last_name})
        if not client_data:
            raise HTTPException(status_code=404, detail="Client not found")
        phones = []
        for phone in client_data.get("phone_list", []):
            phones.append(Phone(**phone))
        return phones
