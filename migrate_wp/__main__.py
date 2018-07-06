"""Utilitaire de migration du site vitrine vers WordPress"""

import re
import locale
import configparser

import click

from . import Importer, Parser, Article, API

locale.setlocale(locale.LC_ALL, 'fr-FR')

@click.command()
@click.option('-c', '--config', 'config_file', default="config.cfg", type=click.File('r'))
def main(config_file):
    """Utilitaire de migration du site vitrine AdA Risques"""
    config = configparser.ConfigParser()
    config.read_file(config_file)

    importer = Importer(config['Database'])
    parser = Parser(importer.public_files())

    api = API(config['API'], importer.indexes(), config['Categories'])
    export = []
    
    for cat in importer.categories():
        export.append(Article(cat))

    for art in importer.articles():
        export.append(Article.parse(art, parser))

    for entry in export:
        click.echo('{0}'.format(entry).encode('utf-8'))

        if entry.id in api.indexes:
            req = api.put(entry)
        else:
            req = api.post(entry)

        if req.status_code not in (200, 201, 204):
            click.echo(api.json(entry))
            click.echo("{0.status_code}: {1[message]}".format(req, req.json()))
            click.echo(req.request.url)
            return

        # Affiche les tags non traités
        for match in re.findall(r"\[/?([a-zA-Z0-9]+)(?:=([^\]]*))?\]", entry.content):
            click.echo('\t{0}'.format(match).encode('utf-8'))

    importer.save_indexes(api.indexes)

if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()
