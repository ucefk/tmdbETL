import psycopg2
from config import Config


config = Config()

class SqlQueries:
    def __init__(self):
        self.db_host = config.db_host
        self.db_port = config.db_port
        self.db_name = config.db_name
        self.db_user = config.db_user
        self.db_password = config.db_password

    # Connect to the database
    def execute_query(self, query, data=None, fetch=False):
        conn = psycopg2.connect(
            host=self.db_host,
            port=self.db_port,
            dbname=self.db_name,
            user=self.db_user,
            password=self.db_password
        )
        with conn:
            with conn.cursor() as cur:
                if data:
                    cur.executemany(query, data)
                else:
                    cur.execute(query)
        conn.close()

    # Delete a table
    def drop_table(self, table):
        query = '''
        DROP TABLE IF EXISTS {}
        '''.format(table)
        self.execute_query(query)

    # Create a table
    def create_table(self, table):
        query = '''
            CREATE TABLE IF NOT EXISTS {} (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                release_date DATE NOT NULL,
                genres VARCHAR(255) NOT NULL
        )
        '''.format(table)
        self.execute_query(query)

    # Insert data in table
    def insert_data(self, table, df):
        data = df.values.tolist()
        query = '''
            INSERT INTO {} (id, title, release_date, genres)
            VALUES (%s, %s, %s, %s);
        '''.format(table)
        self.execute_query(query, data)
