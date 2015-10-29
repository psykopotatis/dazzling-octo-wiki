from base import BaseHandler

class IndexPage(BaseHandler):
    def get(self):
        self.render('/templates/index.html')
