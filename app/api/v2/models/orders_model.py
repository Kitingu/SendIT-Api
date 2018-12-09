from db_init import db
import datetime
import psycopg2.extras

class OrderModel:
    """blueprint for creating a parcel delivery order"""

    def __init__(self, sender_name, user_id, receiver_name, receiver_contact, weight, pickup_location, destination):
        """function to create parcel orders """

        price = 50 * int(weight)
        self.sender_name = sender_name,
        self.user_id = user_id
        self.receiver_name = receiver_name,
        self.receiver_contact = receiver_contact,
        self.weight = int(weight),
        self.pickup_location = pickup_location,
        self.current_location = pickup_location,
        self.destination = destination,
        self.price = 'Ksh' + str(price),
        self.status = "on-transit"
        self.time_created = datetime.datetime.utcnow().strftime('%B %d %Y - %H:%M:%S')

    def create_order(self):
        """method for creating a parcel delivery order"""
        try:
            with db as connection:
                cursor = connection.cursor()
                cursor.execute(
                    """
                    INSERT INTO parcels(sender_name, user_id, receiver_name, receiver_contact, weight,pickup_location,
                    current_location,destination,price,status,time_created)
                    VALUES(%s, %s, %s, %s, %s,%s, %s, %s, %s,%s,%s) 
                    """,
                    (self.sender_name, self.user_id, self.receiver_name, self.receiver_contact, self.weight,
                    self.pickup_location, self.current_location, self.destination, self.price,
                    self.status, self.time_created)
                )
                return {"message": "order created successfully"}
        except Exception as e:
             return {"Message": e}

    @classmethod
    def get_all_orders(cls):
        """ function that allows the user view all orders"""
        with db as connection:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("SELECT * FROM parcels ORDER BY parcel_id")
            parcels = cursor.fetchall()
            if parcels:
                all_parcels = []
                for parcel in parcels:
                    parcel = cls.display_order(parcel)
                    all_parcels.append(parcel)
                return all_parcels
            return {"message": "no parcels available"}

    @classmethod
    def get_single_order(cls,order_id):
        """function that allows user to get a single order"""
        with db as connection:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute(
                "SELECT * FROM parcels WHERE parcel_id = %s ", (order_id,))
            parcel = cursor.fetchone()
            if parcel:
                return cls.display_order(parcel)
            

    @classmethod
    def cancel_order(cls, parcel_id, user_id):
        """cancel an order only if its not delivered"""
        try:
            order = cls.cancelled_or_delivered(parcel_id)

            if order:
                with db as connection:
                    cursor = connection.cursor()
                    cursor.execute("UPDATE parcels SET status=%s WHERE parcel_id = %s and user_id=%s",
                                    ('cancelled', parcel_id, user_id))
                    return {"message": "order cancelled successfully"}
            return {"message": "order is either cancelled or already delivered"}
        except Exception as error:
            return {"message": error}

    @classmethod
    def update_destination(cls, parcel_id, destination, user_id):
        """change order destination"""
        order = cls.cancelled_or_delivered(parcel_id)

        if order:
            with db as connection:
                cursor = connection.cursor()
                cursor.execute("""UPDATE parcels SET destination =%s WHERE parcel_id = %s AND user_id = %s""",
                                (destination, parcel_id, user_id))
                return {"message": "order updated successfully"}
        return {"order is either cancelled or already delivered"}

    @classmethod
    def change_status(cls, parcel_id, status):
        """change order destination"""
        order = cls.cancelled_or_delivered(parcel_id)

        if order:
            with db as connection:
                cursor = connection.cursor()
                cursor.execute("""UPDATE parcels SET status =%s WHERE parcel_id = %s """,
                                (status, parcel_id))
                return {"message": "order updated successfully"}
        return {"order is either cancelled or already delivered"}

    @classmethod
    def change_location(cls, parcel_id, current_location):
        """ function that allows the admin user to change current location"""
        order = cls.cancelled_or_delivered(parcel_id)

        if order:
            with db as connection:
                cursor = connection.cursor()
                cursor.execute("""UPDATE parcels SET current_location =%s WHERE parcel_id = %s""", (current_location,
                                                                                                    parcel_id))
            return {"message": cls.get_single_order(parcel_id)}

    @staticmethod
    def check_exists(parcel_id):
        """method that checks if a parcel delivery order already exists"""
        try:
            with db as connection:
                cursor = connection.cursor()
                cursor.execute(
                    "SELECT * FROM parcels WHERE parcel_id = %s ", (parcel_id,))

                if cursor.fetchone() is not None:
                    return True
        except Exception as error:
            return {"Message": error}

    @staticmethod
    def cancelled_or_delivered(parcel_id):
        """method for cancelling a parcel delivery order"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM parcels WHERE parcel_id = %s AND status = 'on-transit'",
                            (parcel_id,))
            order = cursor.fetchone()
            if order:
                return True

    @staticmethod
    def get_all_orders_by_user(user_id):
        """method for getting orders made by a specific user"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM parcels WHERE user_id = %s", (user_id,))
            order = cursor.fetchall()
            return order

    @staticmethod
    def check_user(parcel_id):
        """method for checking the owner of a parcel delivery order"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT user_id from parcels WHERE parcel_id = %s",(parcel_id,))
            user_id = cursor.fetchone()
            return user_id[0]

    
    @staticmethod
    def display_order(order_payload):
        payload = {"parcel_id": order_payload["parcel_id"],
                   "user_id": order_payload["user_id"],
                   "sender_name": order_payload["sender_name"],
                   "receiver_name": order_payload["receiver_name"],
                   "receiver_contact": order_payload["receiver_contact"],
                   "weight": order_payload["weight"],
                   "pickup_location": order_payload["pickup_location"],
                   "current_location": order_payload["current_location"],
                   "destination": order_payload["destination"],
                   "price": order_payload["price"],
                   "status": order_payload["status"],
                   "time_created": order_payload["time_created"]
                   }
        return payload