"""API"""

import requests

codes = requests.codes

class API:
    """Classe API"""
    def __init__(self, config, indexes, categories):
        self.config = config
        self.sess = requests.Session()
        self.sess.auth = (config.get('username'), config.get('password'))
        self.indexes = indexes
        self.categories = categories

    def test(self):
        return self.sess.put("{0}wp/v2/pages/19".format(self.config.get('url')))

    def json(self, article):
        json = {
            'date': article.date.isoformat(),
            #'slug': article.slug,
            'status': 'publish',
            'title': article.title,
            'content': article.content
        }
        
        #if article.id in self.indexes:
        #    json['id'] = self.indexes[article.id]

        if article.is_page:
            if article.parent != 0:
                json['parent'] = self.indexes.get(article.parent, 0)
                json['menu_order'] = article.order
        else:
            if article.parent in self.categories:
                json['categories'] = [self.categories[str(article.parent)]]

        return json
    
    def url(self, article, with_id=True):
        """Retourne l'URL pour l'article"""
        shown_id = "/{0}".format(self.indexes.get(article.id)) if with_id else ""
        
        if article.is_page: # Page
            url = "{0}wp/v2/pages{1}".format(self.config.get('url'), shown_id)
        else:
            url = "{0}wp/v2/posts{1}".format(self.config.get('url'), shown_id)
        return url
        
    def put(self, article):
        """Put article to WordPress"""
        req = self.sess.put(self.url(article), json=self.json(article))
        return req
    
    def post(self, article):
        """Put article to WordPress"""
        req = self.sess.post(self.url(article, False), json=self.json(article))
        if req.status_code in (200, 201, 204):
            self.indexes[article.id] = req.json().get('id')
        return req