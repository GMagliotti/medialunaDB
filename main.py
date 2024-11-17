from fastapi import FastAPI
from persistence.cassandra_connection import CassandraConnection
from controllers.client_controller import client_router

cassandra_client = CassandraConnection(["cassandra1", "cassandra2", "cassandra3"], 9042)

app = FastAPI()

app.include_router(client_router, prefix="/clients", tags=["clients"])


@app.get("/")
def read_root():
    return {"message": "Welcome to the API!"}


@app.on_event("startup")
async def startup_event():
    print("API started. Connections established.")


@app.on_event("shutdown")
async def shutdown_event():
    mongo_client.close()
    cassandra_client.close()
    print("Connections finished.")
