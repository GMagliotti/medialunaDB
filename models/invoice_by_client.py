from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class InvoiceByClient(Model):
    __keyspace__ = "invoices"
    client_id = columns.Integer(primary_key=True)
    invoice_id = columns.Integer(primary_key=True, clustering_order="DESC")
    date = columns.Date(primary_key=True, clustering_order="DESC")
    total_with_tax = columns.Float(primary_key=True, clustering_order="DESC")
    tax = columns.Float(index=True)
