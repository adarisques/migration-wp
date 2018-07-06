"""Modèle d'article"""

import re
import unicodedata

from .parser import strip_tags

class Article:
    """Classe article"""
    def __init__(self, article):
        self.title = article['title']
        self.subtitle = article.get('subtitle', None)
        self.content = article.get('content', '')
        self.date = article['date']
        self.id = article.get('id', 0) # pylint: disable=invalid-name
        self.parent = article.get('parent', 0)
        self.order = article.get('order', 0)
        self.is_page = article.get('is_page', True)

    @classmethod
    def parse(cls, article, parser):
        """Retourne un Article parsé"""
        parsed = parser.parse_text(article['content'])
        (title, _, content) = parsed.partition('\n')
        article['is_page'] = article['title'] is not None
        if article['is_page']:
            article['subtitle'] = strip_tags(title).strip()
            article['content'] = parsed
            article['is_page'] = True
        else:
            article['title'] = strip_tags(title).strip()
            article['subtitle'] = None
            article['content'] = content
        return cls(article)

    @property
    def slug(self):
        """Retourne un slug d'article"""
        slug = re.sub(r"[dl]['’]|[\(\)]", r"", self.title.lower())
        slug = unicodedata.normalize('NFKD', slug).encode('ascii', 'ignore').decode('ascii')
        slug = re.sub(r"\b(a|des?|du|et|les?|la)\b", r"", slug)
        slug = re.sub(r"[^a-z0-9]+", r"-", slug)
        slug = slug.strip('-')
        return slug

    def __str__(self):
        return '{s.date:%x} ({s.id:2} in {s.parent:2})\t{s.title} ({s.subtitle})'.format(s=self)
