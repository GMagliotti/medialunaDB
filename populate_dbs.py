import pandas as pd
from persistence.cassandra_connection import CassandraConnection
from models.invoice_by_client import InvoiceByClient
from models.invoice_by_product import InvoiceByProduct
from datetime import datetime


def main():
    invoice_df = pd.read_csv("data/e01_factura.csv", sep=";")
    invoice_details_df = pd.read_csv("data/e01_detalle_factura.csv", sep=";")
    client_df = pd.read_csv("data/e01_cliente.csv", sep=";", encoding="latin1")
    phone_df = pd.read_csv("data/e01_telefono.csv", sep=";")
    product_df = pd.read_csv("data/e01_producto.csv", sep=";")

    joined_invoice = pd.merge(invoice_df, invoice_details_df, on="nro_factura")
    joined_client = pd.merge(client_df, phone_df, on="nro_cliente")

    cassandra_client = CassandraConnection()
    cassandra_client.set_default_keyspace("invoices")
    for index, row in joined_invoice.iterrows():
        print(row)
        InvoiceByClient.create(
            client_id=row["nro_cliente"],
            product_id=row["codigo_producto"],
            date=row["fecha"],
            invoice_id=row["nro_factura"],
            item_number=row["nro_item"],
            total_with_tax=row["total_con_iva"],
            tax=row["iva"],
            amount=row["cantidad"],
        )
        InvoiceByProduct.create(
            client_id=row["nro_cliente"],
            product_id=row["codigo_producto"],
            date=row["fecha"],
            invoice_id=row["nro_factura"],
            item_number=row["nro_item"],
            total_with_tax=row["total_con_iva"],
            tax=row["iva"],
            amount=row["cantidad"],
        )


if __name__ == "__main__":
    main()
