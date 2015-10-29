import webapp2
from index import IndexPage
from signup import SignupPage
from welcome import WelcomePage
from login import LoginPage
from logout import LogoutPage

app = webapp2.WSGIApplication([
    (r'/', IndexPage),
    (r'/signup', SignupPage),
    (r'/welcome', WelcomePage),
    (r'/login', LoginPage),
    (r'/logout', LogoutPage),
], debug=True)
