orders = {}


class OrdersModel:
    def __init__(self):
        self.db = orders

    def create_order(self, sender_name, receiver_name, receiver_contact, weight, pickup_location, destination
                     ):
        """function to create percel orders """
        parcel_id = len(self.db) + 1
        price = 50 * weight
        self.db[parcel_id] = {
            "sender_name": sender_name,
            "receiver_name": receiver_name,
            "receiver_contact": receiver_contact,
            "weight": weight,
            "pickup_location": pickup_location,
            "current_location": pickup_location,
            "destination": destination,
            "price": price,
            "status": "on-transit"
        }

    def get_all_order(self):
        """ function that allows the user view all orders"""
        return self.db

    def get_single_order(self, parcel_id):
        if parcel_id in self.db:
            return self.db[parcel_id]

    def delete_order(self, parcel_id):
        del self.db[parcel_id]

    def update_order(self, parcel_id, status):
        order = self.get_single_order(parcel_id)
        if order:
            order['status'] = status
            return order


# ben = OrdersModel()
# print(ben.create_order("benedict", "alfred mutua", "bendeh@gmail.com", 10, "Kisumu", "Nairobi"))
# # print(ben.get_all_order())
# print(ben.get_single_order(1))
