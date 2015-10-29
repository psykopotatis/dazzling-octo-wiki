from google.appengine.ext import db
import random
import string
import hashlib

def make_salt():
    return ''.join(random.choice(string.ascii_lowercase) for x in range(5))

def make_password_hash(name, password, salt=None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + password + salt).hexdigest()
    print('cookie hash: ' + h)
    return "%s|%s" % (h, salt)

def validate_password(name, password, h):
    salt = h.split('|')[1]
    print('cookie: ' + h)
    print('cookie salt: ' + salt)
    password_hash = make_password_hash(name, password, salt)
    print('generated cookie: ' + password_hash)
    return h == make_password_hash(name, password, salt)

def users_key(group='default'):
    return db.Key.from_path('users', group)
