"""Fonctions d'import de données"""

import json
from datetime import datetime
from os.path import basename, splitext

class Importer:
    '''Classe d'import depuis les exports PHPMyAdmin'''
    def __init__(self, tables):
        self.tables = tables

    def load_table(self, table):
        """Importe une table depuis un fichier JSON exporté depuis PHPMyAdmin"""
        if table in self.tables:
            with open(self.tables[table]) as file:
                table_name = splitext(basename(self.tables[table]))[0]
                for row in json.load(file):
                    if row['type'] == 'table' and row['name'] == table_name:
                        return row['data']
            return []
        return []
    
    def indexes(self):
        try:
            with open(self.tables['indexes']) as file:
                return json.load(file)
        except FileNotFoundError:
            return dict()
    
    def save_indexes(self, indexes):
        with open(self.tables['indexes'], 'w') as file:
            json.dump(indexes, file)

    def categories(self):
        """Retourne la liste des catéggories en base"""
        categories = []
        for cat in self.load_table('categories'):
            categories.append({
                'id': "R{0}".format(cat['id']),
                'parent': "0",
                'order': int(cat['rang']),
                'date': datetime.fromtimestamp(int(cat['date'])),
                'title': cat['nomRubrique'],
            })
        return sorted(categories, key=lambda cat: (cat['parent'], cat['order']))
    
    def articles(self):
        """Retourne la liste des articles en base"""
        articles = []
        subcategories = {}
        
        for sub in self.load_table('subcategories'):
            subcategories[int(sub['id'])]= ({
                'id': "S{0}".format(sub['id']),
                'parent': "R{0}".format(sub['idRubrique']),
                'order': int(sub['rang']),
                'title': sub['nomSousRubrique'],
            })

        for art in self.load_table('articles'):
            sub = subcategories[int(art['sousRubrique'])]
            page = int(art['sousRubrique']) not in (20, 43)
            article = {
                'id': sub['id'] if page else "A{0}".format(art['id']),
                'parent': sub['parent'] if page else "S{0}".format(art['sousRubrique']),
                'order': sub['order'] if page else 0,
                'date': datetime.fromtimestamp(int(art['date'])),
                'title': sub['title'] if page else None,
                'content': art['article']
            }
            if "-" not in article['parent']:
                articles.append(article)
        return sorted(articles, key=lambda art: (art['parent'], art['order']))

    def public_files(self):
        """Associe le descriptif des fichiers à leur identifiant"""
        files = {}
        for file in self.load_table('publicfiles'):
            files[file['id']] = {
                'id': int(file['id']),
                'type': file['type'],
                'name': file['nom'],
                'comment': file['commentaires']
            }
        return files
