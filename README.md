## Utilitaire de migration du site vitrine vers WordPress

### Installation

Nécessite Python 3 avec virtualenv.

Créer un environnement virtuel puis installer les dépendances :

```bash
virtualenv venv
source venv/bin/activate
pip install -r requirements.py
```
`source venv/Script/activate` sous Windows

### Configuration

4 tables doivent être exportées depuis PHPMyAdmin au format JSON :
- `ada_articles`
- `ada_sous_rubriques`
- `ada_rubriques`
- `enet_v2_gestion_fichiers_public`

Les exports pourront être placés dans un répertoire `data` ou à tout autre emplacement

Un fichier de configuration (`config.cfg` par défaut) doit ensuite être créé :

```ini
[Database]

# Chemins vers les 4 tables téléchargées
Articles = data/ada_articles.json
PublicFiles = data/enet_v2_gestion_fichiers_public.json
Categories = data/ada_rubriques.json
SubCategories = data/ada_sous_rubriques.json

# Et fichier de correspondance entre les anciens et nouveaux index (sera créé automatiquement)
Indexes = data/indexes.json

[Categories]
# Correspondance entre les anciennes et nouvelles catégories d'articles
# Les nouvelles catégories doivent être créées manuellement dans WordPress.

# Evénements
20 = 5

# Culturisque
43 = 6

[API]
Url = <Adresse de l'API WordPress>
Username = <Nom d'utilisateur WordPress>
Password = <Mot de passe WordPress>
```

### Utilisation

Ensuite, exécuter :
```bash
python -m migrate_wp
```