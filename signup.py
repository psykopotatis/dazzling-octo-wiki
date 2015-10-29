from models import User
from base import BaseHandler


class SignupPage(BaseHandler):
    def render_page(self, username='', password='', verify='', email='', error='', next_url=''):
        self.render('/templates/signup.html', username=username, password=password, verify=verify,
                    email=email, error=error, next_url=next_url)

    def get(self):
        next_url = self.request.headers.get('referer', '/')
        self.render_page(next_url=next_url)

    def post(self):
        print('[POST]', self.request)
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        # Signup on any page and get redirected to that page when complete.
        next_url = str(self.request.get('referer'))
        if not next_url or next_url.startswith('/login'):
            next_url = '/'

        if username and password and verify:
            existing_user = User.by_name(username)
            # Make sure user doesnt already exists
            if existing_user:
                error = 'Error, user already exists: ' + username
                self.render_page(username, password, verify, email, error)
            else:
                new_user = User.register(username, password, email)
                new_user.put()

                self.set_secure_cookie('userId', str(new_user.key().id()))

                # Redirect to the referring page
                self.redirect(next_url)
        else:
            error = 'Error, you need to fill in all values.'
            self.render_page(username, password, verify, email, error, next_url=next_url)
