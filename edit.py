from models import Wiki, VersionedWikiContent
from base import BaseHandler
import time

class EditPage(BaseHandler):
    def get(self, page):
        wiki = Wiki.get_by_page(page)
        content = ''
        if wiki:
            version = self.request.get('v')
            if version:
                versioned_wiki = Wiki.get_version(wiki, int(version))
                content = versioned_wiki.content
            else:
                latest_wiki = Wiki.get_latest(wiki)
                content = latest_wiki.content

        self.render('/templates/edit.html', page=page, content=content)

    def post(self, page):
        content = self.request.get('content')
        creator = self.user

        wiki = Wiki.get_by_page(page)
        latest_version = Wiki.get_latest(wiki)
        version = latest_version.version + 1 if latest_version else 1

        if not wiki:
            wiki = Wiki(page=page)
            wiki.put()

        versioned_content = VersionedWikiContent(version=version, content=content, creator=creator, wiki=wiki)
        versioned_content.put()

        time.sleep(2)

        self.redirect(page)
