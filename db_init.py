from manage import Database

db = Database()


def create_tables():
    TABLES_SCHEMA = (
        """
                CREATE TABLE IF NOT EXISTS users(
                    user_id SERIAL PRIMARY KEY,
                    username VARCHAR(140) UNIQUE NOT NULL,
                    password VARCHAR(140) NOT NULL,
                    email VARCHAR ,
                    admin BOOL NOT NULL,
                    date_created TIMESTAMP 
                )
                """,

        """
        CREATE TABLE IF NOT EXISTS parcels(
            parcel_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
            sender_name VARCHAR(140) NOT NULL,
            receiver_name VARCHAR(140) NOT NULL,
            receiver_contact VARCHAR NOT NULL,
            weight VARCHAR NOT NULL,
            pickup_location VARCHAR(140) NOT NULL,
            current_location VARCHAR(140) NULL,
            destination VARCHAR(140) NOT NULL,
            price VARCHAR(140) NOT NULL,
            status VARCHAR(140) NOT NULL,
            time_created TIMESTAMP 
        )
        """

    )
    for command in TABLES_SCHEMA:
        db.create_tables(command)


create_tables()
