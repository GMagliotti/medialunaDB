from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class InvoiceByClient(Model):
    __keyspace__ = "invoices"
    client_id = columns.Integer(primary_key=True)
    product_id = columns.Integer()
    date = columns.Date(primary_key=True, clustering_order="DESC")
    invoice_id = columns.Integer(index=True)
    item_number = columns.Integer(index=True)
    total_with_tax = columns.Float(index=True)
    tax = columns.Float(index=True)
    amount = columns.Float(index=True)
