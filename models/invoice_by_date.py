from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class InvoiceByDate(Model):
    __keyspace__ = "invoices"
    id = columns.Integer(primary_key=True, default=1)
    date = columns.Date(primary_key=True, clustering_order="DESC")
    client_id = columns.Integer(primary_key=True, clustering_order="DESC")
    invoice_id = columns.Integer(primary_key=True, clustering_order="DESC")
    total_with_tax = columns.Float(primary_key=True, clustering_order="DESC")
    tax = columns.Float(index=True)
