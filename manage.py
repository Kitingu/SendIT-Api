import psycopg2


class Database:
    def __init__(self):
        self.connection = psycopg2.connect(
            host="localhost",
            user="postgres",
            dbname="postgres",
            password="bendeh911"
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
