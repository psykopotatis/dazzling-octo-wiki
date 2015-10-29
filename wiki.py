from base import BaseHandler
from models import Wiki

class WikiPage(BaseHandler):
    def get(self, page):
        wiki = Wiki.get_by_page(page)
        if wiki:
            wikis = []
            if page == '/':
                wikis = Wiki.get_all()
            self.render('/templates/wiki.html', page=page, content=wiki.content, wikis=wikis)
        else:
            self.redirect('/_edit' + page)
