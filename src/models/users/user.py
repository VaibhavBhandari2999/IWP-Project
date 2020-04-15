import uuid
from src.common.utils1 import Utils
from src.common.database import Database
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
__author__="Vaibhav"


class User():
    def __init__(self, email, password, username,_id=None):
        self.email = email
        self.password = password
        self.username = username
        self._id= uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        user_data = Database.find_one(UserConstants.COLLECTION,{"email":email}) #Password in sha512 -> pbkdf
        print(email)

        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist")

        #print(user_data)
        if not Utils.check_hashed_password(password, user_data['password']):
            raise UserErrors.IncorrectPasswordError("Your password was wrong")

        return True


    @staticmethod
    def register_user(email,password,username):
        user_data = Database.find_one("users", {"email": email})  # Password in sha512 -> pbkdf

        if user_data is not None:
            raise UserErrors.UserAlreadyRegistered("The e-mail you registered already exists")

        if not Utils.email_is_valid(email):
            raise UserErrors.InvalidEmailError("The email does not have right format")
        User(email, Utils.hash_password(password), username).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.json())


    def json(self):
        return {
            "_id"  : self._id,
            "email" : self.email,
            "password" : self.password,
            "username" : self.username
        }

    @classmethod
    def find_by_email(cls,email):
        return cls(**Database.find_one(UserConstants.COLLECTION,{'email':email}))
