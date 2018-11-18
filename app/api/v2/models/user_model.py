from manage import db


class UserModel:

    def __init__(self, email, username, password, user_id):
        """initialize an instance of the user class"""
        self.email = email,
        self.username = username,
        self.password = password,
        self.admin = False
        self.user_id = user_id,

    def create_user(self):
        try:
            db.cursor.execute("INSERT INTO users (email,first_name,last_name,password) \
                                VALUES (%s, %s, %s, %s)", (self.email, self.first_name,
                                                           self.last_name, self.password))
            return {"message": "user registered successfully"}
        except Exception as e:
            return {"Message": e}

    @staticmethod
    def get_single_user(email):
        db.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

    @staticmethod
    def get_all_users():
        db.cursor.execute("SELECT * FROM users ORDER BY email")
        users = db.cursor.fetchall()
        data = []
        for k, v in enumerate(users):
            email, user_id, first_name, last_name = v
            user = {
                "email": email,
                "user_id": user_id,
                "first_name": first_name,
                "last_name": last_name
            }
            data.append(user)
        return data

    @classmethod
    def update_user(cls, email, password):
        db.cursor.execute("UPDATE users SET password = %s WHERE email = %s"(email, password))

    @classmethod
    def exists(cls, email):
        db.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = db.cursor.fetchone()
        if user:
            return True
