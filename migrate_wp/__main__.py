"""Utilitaire de migration du site vitrine vers WordPress"""

import re
import locale
from datetime import datetime

import click

from .importer import load_table
from .parser import Parser, make_title, make_slug

locale.setlocale(locale.LC_ALL, 'fr-FR')

@click.command()
@click.argument('articles_table', type=click.File('r'))
@click.argument('public_files_table', type=click.File('r'))
def main(articles_table, public_files_table):
    """Fonction principale"""
    articles = load_table(articles_table, 'ada_articles')
    public_files = load_table(public_files_table, 'enet_v2_gestion_fichiers_public')
    parser = Parser(public_files)

    for article in articles:
        article['id'] = int(article['id'])
        article['sousRubrique'] = int(article['sousRubrique'])
        article['rang'] =  article['rang']

    for article in sorted(articles, key=lambda article: (article['sousRubrique'], article['id'])):
        content = parser.parse_text(article['article'])
        date = datetime.fromtimestamp(int(article['date']))

        (title, _, content) = content.partition('\n')

        title = make_title(title)
        slug = make_slug(title)

        click.echo('{d:%x} ({a[sousRubrique]:2}/{a[id]})\t{t}'.format(
            a=article, d=date, t=title, s=slug).encode('utf8'))

        if article['etat'] != "enCours":
            click.echo(article['etat'])

        for match in re.findall(r"\[/?([a-zA-Z0-9]+)(?:=([^\]]*))?\]", content):
            click.echo('\t{0}'.format(match))

        if article['sousRubrique'] == 20: # Evenements
            pass
        elif article['sousRubrique'] == 43: # Culturisque
            pass
        else:
            if article['id'] == 6:
                click.echo(content)

if __name__ == '__main__':
    # pylint: disable=no-value-for-parameter
    main()
