from pymongo import MongoClient


class MongoConnection:
    def __init__(self, host='localhost', port=27017, database='db', username='root', password='example'):
        # Crea un cliente síncrono de MongoDB con autenticación
        self.client = MongoClient(
            f"mongodb://{username}:{password}@{host}:{port}/{database}?authSource=admin"
        )
        self.db = self.client[database]

    def set_db(self, db_name: str):
        """Permite cambiar la base de datos utilizada"""
        self.db = self.client[db_name]

    def get_db(self):
        """Devuelve la base de datos actual"""
        return self.db

    def get_collection(self, collection_name: str):
        """Devuelve una colección específica"""
        return self.db[collection_name]

    def create_view(self, view_name, view_on, pipeline):
        return self.db.command({
            "create": view_name,
            "viewOn": view_on,
            "pipeline": pipeline
        })

    def drop_view(self, view_name):
        self.db[view_name].drop()

    def close(self):
        """Cierra la conexión con MongoDB"""
        self.client.close()



