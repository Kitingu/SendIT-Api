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
        try:
            user = self.exists(self.username)

            if not user:
                db.cursor.execute("INSERT INTO users (email,username,password,admin,date_created) \
                                    VALUES (%s, %s, %s, %s,%s)", (self.email, self.username,
                                                                  self.password, self.admin, self.date_created))
                db.commit()
                return {"message": "user registered successfully"}
            return {"error": "user already exists"}
        except Exception as error:
            return {"Message": error}

    @staticmethod
    def get_single_user(email):
        """method that returns a single user by their id"""
        db.cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = db.cursor.fetchone()
        return user

    @staticmethod
    def get_all_users():
        """method that returns all users"""
        db.cursor.execute("SELECT * FROM users ORDER BY user_id")
        users = db.cursor.fetchall()
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
        db.cursor.execute(
            "UPDATE users SET password = %s WHERE user_id = %s"(password, user_id))

    @classmethod
    def exists(cls, username):
        """method that checks if a user already exists"""
        db.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = db.cursor.fetchone()

        if user:
            return user
