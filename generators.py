from persistence.mongo_connection import MongoConnection
from typing import Generator


def get_mongo_connection() -> Generator[MongoConnection, None, None]:
    mongo_client = MongoConnection(username='root', password='example', host='mongo', port=27017, database='db')
    try:
        yield mongo_client
    finally:
        mongo_client.close()
