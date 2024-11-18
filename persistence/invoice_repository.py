from persistence.cassandra_connection import CassandraConnection
from models.invoice_by_client import InvoiceByClient
from models.invoice_by_product import InvoiceByProduct
from models.invoice_by_date import InvoiceByDate
from functools import reduce


class InvoiceRepository:
    def __init__(self, connection: CassandraConnection | None = None):
        self.connection = CassandraConnection() if connection else connection

    def get_invoices_client_ids(self):
        return (
            InvoiceByClient.objects()
            .values_list("client_id", flat=True)
            .distinct()
            .all()
        )

    def get_count_by_client(client_id: int):
        return InvoiceByClient.objects().filter(client_id=client_id).count()

    def get_invoices_product_ids():
        return (
            InvoiceByProduct.objects()
            .values_list("product_id", flat=True)
            .distinct()
            .all()
        )

    def get_invoices_by_client_id(client_id: int):
        return InvoiceByClient.objects().filter(client_id=client_id).all()

    def get_invoices_by_product_id(product_id: int):
        return InvoiceByProduct.objects().filter(product_id=product_id).all()

    def get_client_total_expenses(client_id: int):
        return reduce(
            lambda i, t: i.total_with_tax + t,
            InvoiceByClient.objects().filter(client_id=client_id).all(),
            0.0,
        )

    def get_invoices_ordered_by_date(self):
        return InvoiceByDate.objects().all()
