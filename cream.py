from services.product_service import ProductService
from persistence.cassandra_connection import CassandraConnection
from persistence.mongo_connection import MongoConnection

if __name__ == "__main__":
    cassandra_connection = CassandraConnection()
    mongo_connection = MongoConnection()
    ps = ProductService(mongo_connection, cassandra_connection)
    ps.create_view_no_invoice_products()
    prods = ps.get_products_with_no_invoice()