from cassandra.cluster import Cluster

class CassandraConnection:
    def __init__(self, host='localhost', port=9042):
        self.cluster: Cluster = Cluster([host], port=port)
        self.session = self.cluster.connect()

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

