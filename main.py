import webapp2

from signup import SignupPage
from login import LoginPage
from logout import LogoutPage
from edit import EditPage
from wiki import WikiPage

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([
    (r'/signup', SignupPage),
    (r'/login', LoginPage),
    (r'/logout', LogoutPage),
    ('/_edit' + PAGE_RE, EditPage),
    (PAGE_RE, WikiPage),
], debug=True)
