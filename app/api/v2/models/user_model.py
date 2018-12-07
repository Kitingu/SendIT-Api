from manage import db
import datetime


class UserModel:
    """ A blueprint for creating users """

    def __init__(self, email, username, password):
        """initialize an instance of the user class"""
        self.email = email,
        self.username = username,
        self.password = password,
        self.admin = False
        self.date_created = datetime.datetime.utcnow()

    def create_user(self):
        """method that allows user to register"""
        user = self.exists(self.username)
        with db as connection:
            cursor = connection.cursor()
            if not user:
                query="""INSERT INTO users (email,username,password,admin,date_created) 
                                    VALUES (%s, %s, %s, %s,%s)"""
                cursor.execute(query,(self.email, self.username, self.password,
                                                 self.admin, self.date_created))
                return {"message": "user registered successfully"}
        return {"error": "user already exists"}

    @staticmethod
    def get_single_user(email):
        """method that returns a single user by their id"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = db.cursor.fetchone()
            return user

    @staticmethod
    def get_all_users():
        """method that returns all users"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users ORDER BY user_id")
            users = cursor.fetchall()
            data = []

            for keys, values in enumerate(users):
                user_id, username, password, email, admin, date_created = values
                user = {

                    "user_id": user_id,
                    "username": username,
                    "password": password,
                    "email": email,
                    "admin": admin,
                    "date_created": date_created
                }
                data.append(user)
            return data

    @classmethod
    def update_user(cls, user_id, password):
        """method that sets a new user password"""
        with db as connection:
            cursor = connection.cursor()
            query= "UPDATE users SET password = %s WHERE user_id = %s"
            cursor.execute(query,(password, user_id))

    @classmethod
    def exists(cls, username):
        """method that checks if a user already exists"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                return user
