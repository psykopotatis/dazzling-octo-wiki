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


class Wiki(db.Model):
    page = db.StringProperty(required=True)

    @classmethod
    def get_by_page(cls, page):
        return cls.all().filter('page', page).get()

    @classmethod
    def get_latest(cls, wiki):
        if wiki:
            return wiki.versionedwikicontent_set.order('-version')[0]
        else:
            return None

    @classmethod
    def get_version(cls, wiki, version):
        if wiki:
            return wiki.versionedwikicontent_set.filter('version', version).get()
        else:
            return None

    @classmethod
    def get_all_versions(cls, wiki):
        return wiki.versionedwikicontent_set.order('version')

    @classmethod
    def get_all(cls):
        return cls.all()

class VersionedWikiContent(db.Model):
    version = db.IntegerProperty(required=True)
    content = db.TextProperty(required=False)
    created = db.DateTimeProperty(auto_now_add=True)
    creator = db.ReferenceProperty(User)
    wiki = db.ReferenceProperty(Wiki)

    def get_url(self):
        return '%s?v=%s' % (self.wiki.page, self.version)

    def get_edit_url(self):
        return '/_edit%s?v=%s' % (self.wiki.page, self.version)

