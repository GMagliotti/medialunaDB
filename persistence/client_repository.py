from persistence.mongo_connection import MongoConnection
from models.populate.client import Client
from models.populate.phone import Phone


class ClientRepository:
    _COLLECTION_NAME = "clients"

    def __init__(self, host="localhost", port=27017, database="db"):
        # TODO receive the database connection as a parameter
        self.mongo: MongoConnection = MongoConnection()

    def insert_one(self, client: Client):
        return self.mongo.get_collection(self._COLLECTION_NAME).insert_one(
            self._client_to_dict(client)
        )

    def insert_many(self, clients: list[Client]):
        collection = self.mongo.get_collection(self._COLLECTION_NAME)
        client_docs = (self._client_to_dict(client) for client in clients)
        collection.insert_many(client_docs)

    def update_one(self, client: Client):
        self.mongo.get_collection(self._COLLECTION_NAME).update_one(
            filter={"client_id": client.client_id},
            update={"$set": self._client_to_dict(client)},
        )

    def delete_one(self, client: Client):
        self.mongo.get_collection(self._COLLECTION_NAME).delete_one(
            {"client_id": client.client_id}
        )

    def delete_one_by_id(self, client_id: int):
        self.mongo.get_collection(self._COLLECTION_NAME).delete_one(
            {"client_id": client_id}
        )

    def get_clients(self, filter={}, skip: int = 0, limit: int = 0):
        cursor = self.mongo.get_collection(self._COLLECTION_NAME).find(
            filter=filter, skip=int(skip), limit=int(limit), batch_size=100
        )
        with cursor:
            for client in cursor:
                yield self._dict_to_client(client)

    def get_clients_by_name(self, first_name: str, last_name: str, skip=0, limit=0):
        name_filter = {"first_name": first_name, "last_name": last_name}
        return self.get_clients(skip=skip, limit=limit, filter=name_filter)

    def get_phones_with_client(self, skip=0, limit=0):
        pipeline = [
            {
                "$unwind": "$phone_numbers"
            },
            {
                "$project": {
                    "phone_numbers.area_code": 1,
                    "phone_numbers.phone_number": 1,
                    "phone_numbers._type": 1,
                    "client_id": 1,
                    "first_name": 1,
                    "last_name": 1,
                    "address": 1,
                    "active": 1,
                }
            },
        ]

        if skip > 0:
            pipeline.append({"$skip": skip})
        if limit > 0:
            pipeline.append({"$limit": limit})

        return self.mongo.get_collection(self._COLLECTION_NAME).aggregate(
            pipeline, allowDiskUse=True, batchSize=100
        )

    def get_client(self, client_id: int) -> Client:
        return self._dict_to_client(
            self.mongo.get_collection(self._COLLECTION_NAME).find_one(
                {"client_id": client_id}
            )
        )

    def _phone_to_dict(self, phone: Phone) -> dict:
        return {
            "area_code": phone.area_code,
            "phone_number": phone.phone_number,
            "_type": phone._type,
        }

    def _dict_to_phone(self, phone_dict, client_id) -> Phone:
        return Phone(
            phone_dict["area_code"],
            phone_dict["phone_number"],
            phone_dict["_type"],
            client_id,
        )

    def _client_to_dict(self, client: Client):
        return {
            "client_id": client.client_id,
            "first_name": client.first_name,
            "last_name": client.last_name,
            "address": client.address,
            "active": client.active,
            "phone_numbers": [
                self._phone_to_dict(phone) for phone in client.phone_list
            ],
        }

    def _dict_to_client(self, client_dict) -> Client:
        return Client(
            client_dict["client_id"],
            client_dict["first_name"],
            client_dict["last_name"],
            client_dict["address"],
            client_dict["active"],
            [
                self._dict_to_phone(phone, client_dict["client_id"])
                for phone in client_dict["phone_numbers"]
            ],
        )
