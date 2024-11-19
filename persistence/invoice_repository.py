from persistence.cassandra_connection import CassandraConnection
from models.invoice_by_client import InvoiceByClient
from models.invoice_detail import InvoiceDetail
from models.invoice_by_date import InvoiceByDate
from functools import reduce


class InvoiceRepository:
    def __init__(self, connection: CassandraConnection | None = None):
        self.connection = CassandraConnection() if connection else connection

    def get_invoices_client_ids(self):
        return (InvoiceByClient.objects()
                .values_list("client_id", flat=True)
                .distinct()
                .all()
        )

    def get_count_by_client(self, client_id: int):
        return (InvoiceByClient
                .objects()
                .filter(client_id=client_id)
                .values_list("invoice_id", flat=True)
                .count())

    def get_invoices_product_ids(self):
        return list(
            InvoiceDetail.objects()
            .values_list("product_id", flat=True)
            .distinct()
            .all()
        )

    def get_invoices_by_client_id(self, client_id: int):
        invoices_without_detail = InvoiceByClient.objects().filter(client_id=client_id).all()
        
        invoices = []

        for i in invoices_without_detail:
            invoices.append({
                "invoice": i,
                "detail": list(InvoiceDetail.objects().filter(invoice_id=i.invoice_id).allow_filtering().all())
            })
        
        return invoices


    def get_invoices_by_product_id(self, product_id: int):
        details = InvoiceDetail.objects().filter(product_id=product_id).all()
        invoices_ids = frozenset(map(lambda d: d.invoice_id, details))
        invoices = []
        for id in invoices_ids:
            invoices.append({
                "invoice": InvoiceByClient.objects().filter(invoice_id=id).all(),
                "detail": InvoiceDetail.objects().filter(invoice_id=id).all()
            })
        
        return invoices


    def get_client_total_expenses(self, client_id: int):
        return (self
                .connection
                .session
                .execute(f"SELECT SUM(total_with_tax) FROM invoices.invoice_by_client WHERE client_id = {client_id}")[0]
                .system_sum_total_with_tax
        )

    def get_invoices_ordered_by_date(self):
        return InvoiceByDate.objects().all()
    
    def close(self):
        self.connection.close()
