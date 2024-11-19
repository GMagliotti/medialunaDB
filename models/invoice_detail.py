from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class InvoiceDetail(Model):
    __keyspace__ = "invoices"
    product_id = columns.Integer(primary_key=True)
    invoice_id = columns.Integer(primary_key=True, clustering_order="DESC")
    item_number = columns.Integer(primary_key=True, clustering_order="DESC")
    amount = columns.Float(index=True)
