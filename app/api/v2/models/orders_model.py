from db_init import db
import datetime


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

    @staticmethod
    def get_all_orders():
        """ function that allows the user view all orders"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM parcels ORDER BY parcel_id")
            parcels = db.cursor.fetchall()
            data = []
            for k, v in enumerate(parcels):
                parcel_id, sender_name, sender_id, receiver_name, receiver_contact, weight, pickup_location, \
                current_location, destination, \
                price, status, time_created = v
                parcel = {
                    "parcel_id": parcel_id,
                    "sender_id": sender_id,
                    "sender_name": sender_name,
                    "receiver_name": receiver_name,
                    "receiver_contact": receiver_contact,
                    "weight": weight,
                    "pickup_location": pickup_location,
                    "current_location": current_location,
                    "destination": destination,
                    "price": price,
                    "status": status,
                    "time_created": str(time_created)
                }
                data.append(parcel)
            return data

            return {"message": "no parcels available"}

    @staticmethod
    def get_single_order(order_id):
        """function that allows user to get a single order"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT * FROM parcels WHERE parcel_id = %s ", (order_id,))
            parcels = cursor.fetchone()
            my_parcel = {"parcel_id": parcels[0],
                        "sender_id": parcels[1],
                        "sender_name": parcels[2],
                        "receiver_name": parcels[3],
                        "receiver_contact": parcels[4],
                        "weight": parcels[5],
                        "pickup_location": parcels[6],
                        "current_location": parcels[7],
                        "destination": parcels[8],
                        "price": parcels[9],
                        "status": parcels[10],
                        }
            return my_parcel

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
