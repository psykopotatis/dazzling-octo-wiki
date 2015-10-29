from base import BaseHandler
from models import Wiki

class WikiPage(BaseHandler):
    def get(self, page):
        print('wiki "%s"' % page)
        wiki = Wiki.by_page(page)
        content = wiki.content if wiki else ''
        self.render('/templates/wiki.html', page=page, content=content)
