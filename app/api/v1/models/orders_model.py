orders = {}


class OrdersModel:
    def __init__(self):
        self.db = orders

    def create_order(self, **kwargs):
        """function to create percel orders """
        parcel_id = len(self.db) + 1
        price = 50 * int(kwargs['weight'])
        self.db[parcel_id] = {
            "sender_name": kwargs['sender_name'],
            "receiver_name": kwargs['receiver_name'],
            "receiver_contact": kwargs['receiver_contact'],
            "weight": int(kwargs['weight']),
            "pickup_location": kwargs['pickup_location'],
            "current_location": kwargs['pickup_location'],
            "destination": kwargs['destination'],
            "price": 'Ksh' + str(price),
            "status": "on-transit"
        }

    def get_all_order(self):
        """ function that allows the user view all orders"""
        return self.db

    def get_single_order(self, parcel_id):
        """function that allows user to get a single order"""
        if parcel_id in self.db:
            return self.db[parcel_id]

    def delete_order(self, parcel_id):
        """delete an order"""
        del self.db[parcel_id]

    def update_order(self, parcel_id, status):
        """cancel an order only if its not delivered"""
        order = self.get_single_order(parcel_id)
        if order:
            if not order['status'] == 'delivered':
                order['status'] = status
                # return order

    def update_destination(self, parcel_id, destination):
        """change order destination"""
        order = self.get_single_order(parcel_id)
        if order:
            if not order['status'] == 'delivered':
                order['destination'] = destination
                # return order

    def get_by_specific_user(self, sender_name):
        """"""
        order = [order for order in self.db.values(
        ) if order['sender_name'] == sender_name]
        return order
