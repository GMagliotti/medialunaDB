from cassandra.cluster import Cluster
from models.invoice_by_client import InvoiceByClient
from models.invoice_by_product import InvoiceByProduct
from cassandra.cqlengine.management import sync_table
from cassandra.cqlengine import connection


class CassandraConnection:
    def __init__(self, host=["localhost"], port=9042):
        connection.setup(host, "cqlengine", protocol_version=3)
        self.cluster: Cluster = Cluster(host, port=port)
        self.session = self.cluster.connect()
        self.session.execute(
            "CREATE KEYSPACE IF NOT EXISTS invoices WITH REPLICATION = {'class': \'SimpleStrategy\', 'replication_factor': 2}"
        )
        self.session.set_keyspace("invoices")
        sync_table(InvoiceByClient, keyspaces=['invoices'])
        sync_table(InvoiceByProduct, keyspaces=['invoices'])

    def close(self):
        self.cluster.shutdown()

    def get_session(self):
        return self.session

    def get_cluster(self):
        return self.cluster

    def get_keyspace(self):
        return self.session.keyspace

    def set_default_keyspace(self, keyspace):
        self.session.set_keyspace(keyspace)
