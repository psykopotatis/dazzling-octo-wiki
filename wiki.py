from base import BaseHandler
from models import Wiki

class WikiPage(BaseHandler):
    def get(self, page):
        wiki = Wiki.by_page(page)
        if not wiki:
            self.redirect('/_edit' + page)
        else:
            self.render('/templates/wiki.html', page=page, content=wiki.content)
