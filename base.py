import hmac
import os
import logging

import jinja2
import webapp2
import json
from models import User

logging.getLogger().setLevel(logging.DEBUG)

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class BaseHandler(webapp2.RequestHandler):
    @staticmethod
    def hash_str(s):
        secret = 'h3ll012342345'
        # hashlib.md5(s).hexdigest()
        # hmac defaults to the hashlib.md5 constructor.
        return hmac.new(secret, s).hexdigest()

    def make_secure_val(self, val):
        return '%s|%s' % (val, self.hash_str(val))

    def check_secure_val(self, secure_val):
        val = secure_val.split('|')[0]
        # Returns None otherwise
        if secure_val == self.make_secure_val(val):
            return val

    def write(self, *a, **kwargs):
        self.response.write(*a, **kwargs)

    def render_str(self, template, **params):
        # Add user from initialize method
        params['user'] = self.user
        t = JINJA_ENVIRONMENT.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_json(self, data):
        json_txt = json.dumps(data)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_txt)

    def set_secure_cookie(self, name, val):
        cookie_val = self.make_secure_val(val)
        # No expire time, default expires when we close the browser
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))

    def read_secure_cookie(self, name):
        secure_cookie = self.request.cookies.get(name)
        if secure_cookie:
            cookie_val = self.check_secure_val(secure_cookie)
            return cookie_val

    def initialize(self, *a, **kw):
        """
        Runs on every request.
        Checks that user is logged in.

        """
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('userId')
        print('INITIALIZE!')
        print(uid)
        self.user = uid and User.by_id(int(uid))

        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'
