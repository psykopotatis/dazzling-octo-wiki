from base import BaseHandler
from models import Wiki

class WikiPage(BaseHandler):
    def get(self, page):
        wiki = Wiki.get_by_page(page)
        print(wiki)
        if wiki:
            version = self.request.get('v')
            if version:
                versioned_wiki = Wiki.get_version(wiki, int(version))
                content = versioned_wiki.content
            else:
                latest_wiki = Wiki.get_latest(wiki)
                content = latest_wiki.content
            print('v=' + version)
            print('page: ' + wiki.page)
            self.render('/templates/wiki.html', page=page, version=version, content=content)
        else:
            self.redirect('/_edit' + page)
