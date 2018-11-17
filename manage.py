import psycopg2
from instance.config import Config
import os


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host=os.getenv('host'),
            user=os.getenv('user'),
            dbname=os.getenv('dbname'),
            password=os.getenv('password')
        )

        self.cursor = self.connection.cursor()

    def commit(self):
        """commits query commands to the database"""
        self.connection.commit()

    def query_database(self, query_string):
        """function to query the database"""
        self.cursor.execute(query_string)

    def create_tables(self, table):
        """creates table"""
        self.cursor.execute(table)
        self.commit()

    def drop_tables(self, table_name):
        """deletes tables"""
        self.cursor.execute("DROP TABLE IF EXISTS " + table_name + ";")
        self.commit()

    def close(self):
        """closes down the database"""
        self.cursor.close()
        self.connection.close()


db = Database()
