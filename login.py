from base import BaseHandler
from models import User

class LoginPage(BaseHandler):
    def render_page(self, username='', password='', error='', next_url=''):
        self.render('/templates/login.html', username=username, password=password, error=error, next_url=next_url)

    def get(self):
        next_url = self.request.headers.get('referer', '/')
        self.render_page(next_url=next_url)

    def post(self):
        print('[POST]', self.request.POST)
        username = self.request.get('username')
        password = self.request.get('password')

        # Login from any page and get redirected to that page when complete.
        next_url = str(self.request.get('referer'))
        if not next_url or next_url.startswith('/login'):
            next_url = '/'

        if username and password:
            # Fetch user
            user = User.login(username, password)
            if user:
                print('PASSWORD OK')
                # Store user id in secure cookie
                self.set_secure_cookie('userId', str(user.key().id()))
                # Redirect to referring page
                self.redirect(next_url)
            else:
                error = 'Error, username or password wrong.'
                self.render_page(username, password, error, next_url)
        else:
            error = 'Error, you need to fill in all values.'
            self.render_page(username, password, error, next_url)
