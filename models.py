from google.appengine.ext import db
from utils import *


class User(db.Model):
    name = db.StringProperty(required=True)
    password_hash = db.StringProperty(required=True)
    email = db.TextProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)

    @classmethod
    def by_name(cls, name):
        return cls.all().filter('name', name).get()

    @classmethod
    def register(cls, name, password, email):
        password_hash = make_password_hash(name, password)
        return cls(name=name,
                    password_hash=password_hash,
                    email=email)

    @classmethod
    def login(cls, name, password):
        user = cls.by_name(name)
        print(user)
        if user and validate_password(name, password, user.password_hash):
            return user

    def __str__(self):
        return 'User{id:%s, name:%s}' % (self.key().id(), self.name)