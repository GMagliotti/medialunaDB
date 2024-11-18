from persistence.mongo_connection import MongoConnection
from models.populate.client import Client
from models.populate.phone import Phone

class ClientRepository:
    _COLLECTION_NAME = 'clients'

    def __init__(self, host, port, database):
        # TODO receive the database connection as a parameter
        self.mongo: MongoConnection = MongoConnection();

    def insert_one(self, client: Client):
        return self.mongo.get_collection(self._COLLECTION_NAME).insert_one(self._client_to_dict(client))

    def insert_many(self, clients: list[Client]):
        collection = self.mongo.get_collection(self._COLLECTION_NAME)
        client_docs = (self._client_to_dict(client) for client in clients)
        collection.insert_many(client_docs)

    def update_one(self, client: Client):
        self.mongo.get_collection(self._COLLECTION_NAME).update_one(filter={'client_id': client.client_id}, update={'$set': self._client_to_dict(client)})

    def delete_one(self, client: Client):
        self.mongo.get_collection(self._COLLECTION_NAME).delete_one({'client_id': client.client_id})
    
    def delete_one_by_id(self, client_id: int):
        self.mongo.get_collection(self._COLLECTION_NAME).delete_one({'client_id': client_id});

    def get_clients(self, skip = 0, limit = 0, filter = {}):
        cursor = self.mongo.get_collection(self._COLLECTION_NAME).find(filter=filter, skip=skip, limit=limit, batch_size=100);
        with cursor:
            for product in cursor:
                yield self._dict_to_client(product)

    def get_clients_by_name(self, first_name: str, last_name: str, skip = 0, limit = 0):
        name_filter = {"first_name": first_name, "last_name": last_name}
        return self.get_clients(skip=skip, limit=limit, filter=name_filter)
    
    def get_phones_with_client(self, skip = 0, limit = 0):
        pipeline = [
            {"$unwind": "$phone"},  # Unwind the embedded phone list to create a document per phone
            {
                "$project": {
                    "phone.area_code": 1,
                    "phone.phone_number": 1,
                    "phone.type": 1,
                    "client_id": 1,
                    "first_name": 1,
                    "last_name": 1,
                    "address": 1,
                    "active": 1
                }
            }
        ]
        return self.mongo.get_collection(self._COLLECTION_NAME).aggregate(pipeline, allowDiskUse=True, batchSize=100)

    def get_client(self, client_id: int) -> Client:
        return self._dict_to_client(
            self.mongo.get_collection(self._COLLECTION_NAME).find_one({'client_id': client_id})
            );
    
    def _phone_to_dict(self, phone: Phone) -> dict:
        return {
            'area_code': phone.phone_id,
            'phone_number': phone.number,
            'type': phone.type
        }
    
    def _dict_to_phone(self, phone_dict) -> Phone:
        return Phone(
            phone_dict['area_code'],
            phone_dict['phone_number'],
            phone_dict['type']
        )
    
    def _client_to_dict(self, client: Client):
        return {
            'client_id': client.client_id,
            'first_name': client.first_name,
            'last_name': client.last_name,
            'address': client.address,
            'active': client.active,
            'phone_numbers': [self._phone_to_dict(phone) for phone in client.phones]
        }
    
    def _dict_to_client(self, client_dict) -> Client:
        return Client(
            client_dict['client_id'],
            client_dict['first_name'],
            client_dict['last_name'],
            client_dict['address'],
            client_dict['active'],
            [self._dict_to_phone(phone) for phone in client_dict['phone_numbers']]
        )
    
    