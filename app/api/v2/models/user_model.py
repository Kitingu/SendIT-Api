from manage import db
import datetime
import psycopg2.extras

class UserModel:
    """ A blueprint for creating users """

    def __init__(self, email, username, password,admin=False,date_created=datetime.datetime.utcnow()):
        """initialize an instance of the user class"""
        self.email = email,
        self.username = username,
        self.password = password,
        self.admin = admin
        self.date_created = date_created

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
        # return {"error": "user already exists"}

    @classmethod
    def get_single_user(cls,username):
        """method that returns a single user by their id"""
        with db as connection:
            cursor = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            query = "SELECT * FROM users WHERE username = %s"
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            if user:
                return cls.display_user(user)
            return {"message":"user does not exist"}

    @classmethod
    def get_all_users(cls):
        """method that returns all users"""
        with db as connection:
            cursor = connection.cursor(
                cursor_factory=psycopg2.extras.DictCursor)
            cursor.execute("select * from users")
            users = cursor.fetchall()
            if users:
                all_users = []
                for user in users:
                    user=cls.display_user(user)
                    all_users.append(user)
                return all_users
            return {"message":"there are no registered users at the moment"}

    @staticmethod
    def update_user(user_id, password):
        """method that sets a new user password"""
        with db as connection:
            cursor = connection.cursor()
            query= "UPDATE users SET password = %s WHERE user_id = %s"
            cursor.execute(query,(password, user_id))

    @staticmethod
    def exists(username):
        """method that checks if a user already exists"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()

            if user:
                return user

    @staticmethod
    def mailexists(email):
        """method that checks if a user email already exists"""
        with db as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user:
                return user
    @staticmethod
    def display_user(user_payload):
        payload = {"user_id": user_payload["user_id"],
                   "username": user_payload["username"],
                   "email": user_payload["email"],
                   "admin": user_payload["admin"],
                   "password": user_payload["password"],
                   "date_created": user_payload["date_created"]}
        return payload

class Admin(UserModel):
    def __init__(self, email, username, password,admin=False,date_created=datetime.datetime.utcnow()):
        super().__init__(email,username,password,admin,date_created)
        self.admin = True
