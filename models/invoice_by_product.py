from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class InvoiceByProduct(Model):
    __keyspace__ = "invoices"
    product_id = columns.Integer(primary_key=True)
    client_id = columns.Integer(primary_key=True, clustering_order="DESC")
    date = columns.Date(primary_key=True, clustering_order="DESC")
    invoice_id = columns.Integer(primary_key=True, clustering_order="DESC")
    item_number = columns.Integer(primary_key=True, clustering_order="DESC")
    total_with_tax = columns.Float(primary_key=True, clustering_order="DESC")
    tax = columns.Float(index=True)
    amount = columns.Float(index=True)
