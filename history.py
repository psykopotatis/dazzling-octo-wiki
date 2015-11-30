from models import Wiki
from base import BaseHandler

class HistoryPage(BaseHandler):
    def get(self, page):
        wiki = Wiki.get_by_page(page)
        wiki_versions = wiki.get_all_versions(wiki)
        self.render('/templates/history.html', page=page, wiki_versions=wiki_versions)

    def post(self, page):
        content = self.request.get('content')
        creator = self.user

        wiki = Wiki.get_by_page(page)
        if wiki:
            wiki.content = content
            wiki.put()
        else:
            new_wiki = Wiki(page=page, content=content, creator=creator)
            new_wiki.put()

        # Redirect to created/edit page
        self.redirect(page)
