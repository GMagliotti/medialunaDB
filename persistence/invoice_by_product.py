from cassandra.cqlengine import columns
from cassandra.cqlengine import connection
from datetime import datetime
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine.models import Model

class InvoiceByClient(Model):
    product_id      = columns.Integer(primary_key=True)
    client_id       = columns.Integer()
    date            = columns.DateTime(index=True)
    invoice_id      = columns.Integer(index=True, default=uuid.uuid4)
    item_number     = columns.Integer(index=True)
    total_with_tax  = columns.Float(index=True)
    tax             = columns.Float(index=True)
    amount          = columns.Float(index=True)
