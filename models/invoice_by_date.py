from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class InvoiceByDate(Model):
    __keyspace__ = "invoices"
    id = columns.Date(primary_key=True, default=1)
    date = columns.Date(primary_key=True, clustering_order="DESC")
    client_id = columns.Integer(index=True)
    product_id = columns.Integer(index=True)
    invoice_id = columns.Integer(index=True)
    item_number = columns.Integer(index=True)
    total_with_tax = columns.Float(index=True)
    tax = columns.Float(index=True)
    amount = columns.Float(index=True)
