import datetime
import uuid
from flask import session, flash
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

class User(UserMixin):

    def __init__(self, dbUser):
        # when pulled from the database the users credentials are
        # in json format. User() requires a json input to process all
        # user information. This is cleaner than including all values
        # in a sequence.
        self._id = str(dbUser[0])
        self.name = dbUser[1]
        self.email = dbUser[2]
        # self.role = json['role']
        self.password = dbUser[3]
        self.image = bytes(dbUser[4]).decode('utf-8')
        self.theme = dbUser[5]
        self.google_account = dbUser[6]


    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self._id

    def has_google_login(self):
        if self.google_account:
            return True
        else:
            return False

    # returns true if user is admin.
    def is_admin(self):
        if self.role == 'admin':
            return True
        else:
            return False

    def json(self):
        return {
            "_id": self._id,
            "name": self.name,
            "email": self.email,
            # "role": self.role,
            "password": self.password,
            "pic": self.image,
            "theme": self.theme
        }