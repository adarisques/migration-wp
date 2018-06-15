"""Fonctions d'import de données"""

import json

def load_table(file, table):
    """Importe une table depuis un fichier JSON exporté depuis PHPMyAdmin"""
    for row in json.load(file):
        if row['type'] == 'table' and row['name'] == table:
            return row['data']
    return []

def map_public_files(public_files):
    """Associe le descriptif des fichiers à leur identifiant"""
    files = {}
    for file in public_files:
        files[file['id']] = {
            'id': file['id'],
            'type': file['type'],
            'name': file['nom'],
            'comment': file['commentaires']
        }
    return files
