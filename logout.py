from base import BaseHandler

class LogoutPage(BaseHandler):
    def get(self):
        for cookie in self.request.cookies:
            self.response.delete_cookie(cookie)
        self.redirect('/')
