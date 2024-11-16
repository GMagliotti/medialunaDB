import pandas as pd
from cassandra.cqlengine.query import LWTException
from persistence.cassandra_connection import CassandraConnection
from persistence.mongo_connection import MongoConnection
from models.invoice_by_client import InvoiceByClient
from models.invoice_by_product import InvoiceByProduct
from models.populate.client import Client
from models.populate.product import Product
from models.populate.phone import Phone


def populate_mongo(client_df, phone_df, product_df, mongo_client):
    """Populate MongoDB with client and product data."""
    db = mongo_client.get_db()

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
                phone_list=[]
            )

    # Add phones to the clients
    for _, row in phone_df.iterrows():
        phone = Phone(
            area_code=row["codigo_area"],
            phone_number=row["nro_telefono"],
            type=row["tipo"],
            client_id=row["nro_cliente"]
        )
        phone_dict = phone.__dict__  # Convert Phone instance to a dictionary
        clients[row["nro_cliente"]].phone_list.append(phone_dict)

    # Upsert clients into MongoDB
    collection = db["clients"]
    for client in clients.values():
        collection.update_one(
            {"client_id": client.client_id},
            {"$set": client.to_dict()},
            upsert=True
        )

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
                stock=stock
            )
        )

    # Upsert products into MongoDB
    product_collection = db["products"]
    for product in products:
        product_collection.update_one(
            {"product_id": product.product_id},
            {"$set": product.__dict__},
            upsert=True
        )

    print("MongoDB population complete.")


def populate_cassandra(invoice_df, invoice_details_df):
    """Populate Cassandra with invoice data."""
    joined_invoice = pd.merge(invoice_df, invoice_details_df, on="nro_factura")

    cassandra_client = CassandraConnection()
    cassandra_client.set_default_keyspace("invoices")

    for _, row in joined_invoice.iterrows():
        try:
            InvoiceByClient.if_not_exists().create(
                client_id=row["nro_cliente"],
                product_id=row["codigo_producto"],
                date=row["fecha"],
                invoice_id=row["nro_factura"],
                item_number=row["nro_item"],
                total_with_tax=row["total_con_iva"],
                tax=row["iva"],
                amount=row["cantidad"],
            )
            InvoiceByProduct.if_not_exists().create(
                client_id=row["nro_cliente"],
                product_id=row["codigo_producto"],
                date=row["fecha"],
                invoice_id=row["nro_factura"],
                item_number=row["nro_item"],
                total_with_tax=row["total_con_iva"],
                tax=row["iva"],
                amount=row["cantidad"],
            )
        except LWTException as e:
            print(e.existing)

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
    mongo_client = MongoConnection(username='root', password='example', host='localhost', port=27017, database='db')

    # Populate databases
    populate_mongo(client_df, phone_df, product_df, mongo_client)
    populate_cassandra(invoice_df, invoice_details_df)

    # Close MongoDB connection
    mongo_client.close()


if __name__ == "__main__":
    main()



