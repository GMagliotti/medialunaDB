from fastapi import FastAPI
from persistence.mongo_connection import MongoConnection
from persistence.cassandra_connection import CassandraConnection

app = FastAPI()

mongo_client = MongoConnection(username='root', password='example', host='localhost', port=27017, database='db')
cassandra_client = CassandraConnection(["cassandra1", "cassandra2", "cassandra3"], 9042)


@app.on_event("startup")
async def startup_event():
    print("API started. Connections established.")


@app.on_event("shutdown")
async def shutdown_event():
    mongo_client.close()
    cassandra_client.close()
    print("Connections finished.")
