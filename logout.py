from base import BaseHandler

class LogoutPage(BaseHandler):
    def get(self):
        for cookie in self.request.cookies:
            self.response.delete_cookie(cookie)

        next_url = self.request.headers.get('referer', '/')
        self.redirect(next_url)
