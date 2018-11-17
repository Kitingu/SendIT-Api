from manage import Database

db = Database()


def create_tables():
    TABLES_SCHEMA = (
        """
        CREATE TABLE IF NOT EXISTS parcels(
            parcel_id SERIAL PRIMARY KEY,
            sender_name VARCHAR(140) NOT NULL,
            receiver_name VARCHAR(140) NOT NULL,
            receiver_contact VARCHAR NOT NULL,
            weight VARCHAR NOT NULL,
            pickup_location VARCHAR(140) NOT NULL,
            current_location VARCHAR(140) NULL,
            destination VARCHAR(140) NOT NULL,
            price VARCHAR(140) NOT NULL,
            status VARCHAR(140) NOT NULL
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS users(
        email VARCHAR PRIMARY KEY,
            username VARCHAR(140) NOT NULL,
            password VARCHAR(140) NOT NULL,
            user_id VARCHAR(140) NOT NULL,
            admin BOOLEAN NOT NULL
        )
        """
    )

    for command in TABLES_SCHEMA:
        db.create_tables(command)

if __name__== '__main__':
    create_tables()