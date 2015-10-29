from models import Wiki
from base import BaseHandler

class EditPage(BaseHandler):
    def get(self, page):
        wiki = Wiki.by_page(page)
        content = wiki.content if wiki else ''
        self.render('/templates/edit.html', page=page, content=content)

    def post(self, page):
        content = self.request.get('content')
        creator = self.user

        wiki = Wiki.by_page(page)
        if wiki:
            wiki.content = content
            wiki.put()
        else:
            new_wiki = Wiki(page=page, content=content, creator=creator)
            new_wiki.put()

        # Redirect to created/edit page
        self.redirect(page)
