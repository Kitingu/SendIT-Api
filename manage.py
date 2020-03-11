import os
import psycopg2
from instance.config import app_config

env = os.getenv("FLASK_ENV")
url = app_config[env].DATABASE_URI


class Database:
    def __init__(self):

        self.connection = None

        # self.cursor = self.connection.cursor()

    def __enter__(self):
        # picks db_url automatically from env hence we pass in an empty string.
        self.connection = psycopg2.connect('')
        return self.connection

    def __exit__(self,exc_type,exc_val,exc_tb):
        if exc_type or exc_val or exc_tb:
            self.connection.rollback()
            self.connection.close()
        else:
            self.connection.commit()
            self.connection.close()


    def create_tables(self, table):
        """creates table"""
        with Database() as connection:
            cursor = connection.cursor()
            cursor.execute(table)

    def drop_tables(self):
        """deletes tables"""
        with Database() as connection:
            cursor = connection.cursor()
            tables = ["DELETE FROM parcels CASCADE",
                      "DELETE FROM users CASCADE",
                      "ALTER SEQUENCE users_user_id_seq RESTART WITH 1;",
                      "ALTER SEQUENCE parcels_parcel_id_seq RESTART WITH 1;"]
            for table in tables:
                cursor.execute(table)

db = Database()