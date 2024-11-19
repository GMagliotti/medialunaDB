from fastapi import FastAPI
from persistence.cassandra_connection import CassandraConnection
from persistence.mongo_connection import MongoConnection
from controllers.client_controller import client_router
from controllers.invoice_controller import invoice_router
from controllers.product_controller import product_router

cassandra_client = CassandraConnection(["localhost"], 9042)
mongo_client = MongoConnection()

app = FastAPI()

app.include_router(client_router, prefix="/clients", tags=["clients"])
app.include_router(invoice_router, prefix="/invoices", tags=["invoices"])
app.include_router(product_router, prefix="/products", tags=["products"])


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
