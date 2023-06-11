import random
from cassandra.cluster import Cluster


class CassandraManager:
    def __init__(self, hosts, port, keyspace):
        host = random.choice(hosts)
        self.host = host
        self.port = port
        self.keyspace = keyspace
        self.session = None

    def connect(self):
        cluster = Cluster([self.host], port=self.port)
        self.session = cluster.connect(self.keyspace)

    def execute(self, query):
        self.session.execute(query)

    def close(self):
        self.session.shutdown()

    def insert_query(self, table, data):
        preprocessed_data = {}
        for key, val in data.items():
            val, dtype = val
            if dtype == "text" or dtype == "date":
                val = str(val).replace("'", "''")
                val = "'" + val + "'"
            else:
                val = str(val)
            preprocessed_data[key] = val

        cols_names = ", ".join(list(preprocessed_data.keys()))
        values = ", ".join(list(preprocessed_data.values()))
        query = f"INSERT INTO {table} ({cols_names}) VALUES ({values})"
        self.execute(query)

    def insert_image_info(self, table_name, user_id, img_id, img_path, img_description):
        self.insert_query(table_name, 
                            {"user_id": (user_id, "text"),
                             "img_id": (img_id, "text"),
                             "img_path": (img_path, "text"),
                             "img_description": (img_description, "text")})

    def get_image_info(self, table_name, user_id, img_id):
        user_id = str(user_id).replace("'", "''")
        img_id = str(img_id).replace("'", "''")
        query = f"SELECT img_description, img_path FROM {table_name} WHERE user_id='{user_id}' AND img_id='{img_id}'"
        rows = self.session.execute(query)
        return rows

hosts = ["cassandra-node1", "cassandra-node2"]
port = 9042
keyspace = "software_arch_proj"
cassandra_manager = CassandraManager(hosts, port, keyspace)
cassandra_manager.connect()
