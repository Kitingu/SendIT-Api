import uuid

users = {}


class UserModel:

    def __init__(self):
        """initialize a data structure that will act as a database"""
        self.db = users

    def save(self, email, username, password):
        self.db[email] = {
            "username": username,
            "password": password,
            "user_id": str(uuid.uuid4()),
            "admin": False
        }

    def get_single_user(self, email):
        if email in self.db:
            return self.db[email]

    def get_all_users(self):
        return {"users": self.db}

    def update_user(self, email, username, password, confirm_password):
        self.users[email] = {
            "username": username,
            "password": password,
            "confirm_password": confirm_password}

    def exists(self, username):
        for user in self.db.values():
            if user['username'] == username:
                return True
