from manage import db
import datetime

class UserModel:

    def __init__(self, email, username, password):
        """initialize an instance of the user class"""
        self.email = email,
        self.username = username,
        self.password = password,
        self.admin = False
        self.date_created = datetime.datetime.utcnow()

    def create_user(self):
        try:
            user = self.exists(self.username)
            if not user:
                db.cursor.execute("INSERT INTO users (email,username,password,admin,date_created) \
                                    VALUES (%s, %s, %s, %s,%s)", (self.email, self.username,
                                                                self.password,self.admin,self.date_created))
                db.commit()
                return {"message": "user registered successfully"}
            return {"error":"user already exists"}
        except Exception as e:
            return {"Message": e}

    @staticmethod
    def get_single_user(user_id):
        db.cursor.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        user=db.cursor.fetchall()
        return user

    @staticmethod
    def get_all_users():
        db.cursor.execute("SELECT * FROM users ORDER BY user_id")
        users = db.cursor.fetchall()
        data = []
        for k, v in enumerate(users):
            user_id, username,password,email,admin,date_created = v
            user = {

                "user_id": user_id,
                "username": username,
                "email": email,
                "admin": admin,
                "date_created": date_created
            }
            data.append(user)
        return data

    @classmethod
    def update_user(cls, user_id, password):
        db.cursor.execute("UPDATE users SET password = %s WHERE user_id = %s"(password,user_id))

    @classmethod
    def exists(cls, username):
        db.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = db.cursor.fetchone()
        if user:
            return True


