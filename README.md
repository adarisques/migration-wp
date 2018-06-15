## Utilitaire de migration du site vitrine vers WordPress

### Installation

Nécessite Python 3 avec virtualenv.

Créer un environnement virtuel puis installer les dépendances :

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.py
```
### Utilisation

Il faut préalablement extraire avec PHPMyAdmin et au format JSON les tables :
- `ada_articles`, par exemple comme `data/ada_articles.json`
- `enet_v2_gestion_fichiers_public`, par exemple comme `data/ada_fichiers_public.json`

Ensuite, exécuter :
```bash
python -m migrate_wp data/ada_articles.json data/ada_fichiers_public.json
```