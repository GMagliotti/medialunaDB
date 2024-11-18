from persistence.mongo_connection import MongoConnection
from persistence.cassandra_connection import CassandraConnection
from typing import Generator


def get_mongo_connection() -> Generator[MongoConnection, None, None]:
    return MongoConnection(
        username="root", password="example", host="mongo", port=27017, database="db"
    )


def get_cassandra_connection() -> Generator[CassandraConnection, None, None]:
    return CassandraConnection()
