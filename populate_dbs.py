import pandas as pd
from cassandra.cqlengine.query import LWTException
from persistence.cassandra_connection import CassandraConnection
from persistence.mongo_connection import MongoConnection
from persistence.client_repository import ClientRepository
from persistence.product_repository import ProductRepository
from models.invoice_by_client import InvoiceByClient
from models.invoice_detail import InvoiceDetail
from models.invoice_by_date import InvoiceByDate
from models.populate.client import Client
from models.populate.product import Product
from models.populate.phone import Phone


def populate_mongo(client_df, phone_df, product_df, mongo_client):
    """Populate MongoDB with client and product data."""
    client_repo = ClientRepository()
    product_repo = ProductRepository()

    # Populate Clients
    clients = {}
    for _, row in client_df.iterrows():
        client_id = row["nro_cliente"]
        if client_id not in clients:
            clients[client_id] = Client(
                client_id=client_id,
                first_name=row["nombre"],
                last_name=row["apellido"],
                address=row["direccion"],
                active=row["activo"],
                phone_list=[],
            )
    # Add phones to the clients
    for _, row in phone_df.iterrows():
        phone = Phone(
            area_code=row["codigo_area"],
            phone_number=row["nro_telefono"],
            _type=row["tipo"],
            client_id=row["nro_cliente"],
        )
        clients[row["nro_cliente"]].phone_list.append(phone)

    # Populate Products
    products = []
    for _, row in product_df.iterrows():
        brand = row["marca"] if pd.notna(row["marca"]) else ""
        name = row["nombre"] if pd.notna(row["nombre"]) else ""
        description = row["descripcion"] if pd.notna(row["descripcion"]) else ""
        price = row["precio"] if pd.notna(row["precio"]) else 0.0
        stock = row["stock"] if pd.notna(row["stock"]) else 0

        products.append(
            Product(
                product_id=row["codigo_producto"],
                brand=brand,
                name=name,
                description=description,
                price=price,
                stock=stock,
            )
        )
    # Clear database to avoid redundant info
    for client_id in clients.keys():
        client_repo.delete_one_by_id(client_id)

    for product in products:
        product_repo.delete_one(product)

    # Upsert clients into MongoDB
    client_repo.insert_many(clients.values())

    # Upsert products into MongoDB
    product_repo.insert_many(products)

    print("MongoDB population complete.")


def populate_cassandra(invoice_df, invoice_details_df):
    """Populate Cassandra with invoice data."""
    cassandra_client = CassandraConnection()
    cassandra_client.set_default_keyspace("invoices")

    for i, row in invoice_df.iterrows():
        try:
            InvoiceByClient.if_not_exists().create(
                client_id=row["nro_cliente"],
                date=row["fecha"],
                invoice_id=row["nro_factura"],
                total_with_tax=row["total_con_iva"],
                tax=row["iva"],
            )
        except LWTException as e:
            print(f'index: {i} - {e.existing}')
        try:
            InvoiceByDate.if_not_exists().create(
                client_id=row["nro_cliente"],
                date=row["fecha"],
                invoice_id=row["nro_factura"],
                total_with_tax=row["total_con_iva"],
                tax=row["iva"],
            )
        except LWTException as e:
            print(f'index: {i} - {e.existing}')

    for i, row in invoice_details_df.iterrows():
        try:
            InvoiceDetail.if_not_exists().create(
                product_id=row["codigo_producto"],
                invoice_id=row["nro_factura"],
                item_number=row["nro_item"],
                amount=row["cantidad"],
            )
        except LWTException as e:
            print(f'index: {i} - {e.existing}')

    print("Cassandra population complete.")
    cassandra_client.close()


def main():
    # Load data
    invoice_df = pd.read_csv("data/e01_factura.csv", sep=";")
    invoice_details_df = pd.read_csv("data/e01_detalle_factura.csv", sep=";")
    client_df = pd.read_csv("data/e01_cliente.csv", sep=";", encoding="latin1")
    phone_df = pd.read_csv("data/e01_telefono.csv", sep=";")
    product_df = pd.read_csv("data/e01_producto.csv", sep=";")

    # Initialize MongoDB connection (sincrónico)
    mongo_client = MongoConnection(
        username="root", password="example", host="localhost", port=27017, database="db"
    )

    # Populate databases
    populate_mongo(client_df, phone_df, product_df, mongo_client)

    populate_cassandra(invoice_df, invoice_details_df)

    # Close MongoDB connection
    mongo_client.close()


if __name__ == "__main__":
    main()
