# Python Projects

Collection pédagogique d'exemples, d'exercices et de projets Python.

> **Maturité : expérimental / apprentissage.** Les dossiers peuvent servir de
> démonstrations ou de points de départ, mais ne sont pas présentés comme des
> applications prêtes pour la production. Le niveau de finition est documenté
> au plus près de chaque projet lorsqu'il dispose de son propre README.

## Projets structurés dans cette collection

| Projet | Domaine | Point d'entrée |
| --- | --- | --- |
| [`corporate_finance_berk`](corporate_finance_berk/) | Finance d'entreprise | [Guide d'utilisation](corporate_finance_berk/GUIDE_UTILISATION.md) |
| [`peb`](peb/) | Performance énergétique du bâtiment | [Documentation](peb/README.md) |
| [`MobilityMap`](MobilityMap/) | Visualisation de données de mobilité | Application Flask du dossier |
| [`PizzaMama`](PizzaMama/) | Application console et API | Scripts du dossier |
| [`PizzaMamaDjango`](PizzaMamaDjango/) | Application web Django | `manage.py` |
| [`Design Patterns`](Design%20Patterns/) | Patrons de conception | [Documentation](Design%20Patterns/README.md) |

## Laboratoires pédagogiques

- **Fondamentaux :** `Algorithme`, `Questionnaire`, `api`, `scripting`.
- **Data et sciences :** `Python Research`, `Chimie`, `Thermo`, `Dashboard`.
- **Interfaces et web :** `Chatbot`, `kivy`, `scraping`, `youtube downloader`.
- **Architecture et réseau :** `ETL`, `Ethical Hacking`.

Ces dossiers sont des supports d'apprentissage. Leurs dépendances et leur niveau
de finition peuvent varier ; consultez le code du dossier avant exécution.

## Expériences archivées

Trois anciennes extractions (`agent_writer_essay`, `github_project_agent` et
`price_arbitrage_tool`) ont été archivées. Elles ne font pas partie de cette
collection et ne sont plus présentées comme des projets autonomes maintenus.
Cette mention remplace les anciens liens publics, qui pointaient vers des
dépôts privés et archivés.

## Conventions d'organisation

- Le statut expérimental ou utilisable doit être indiqué dans le README du
  projet concerné ; l'absence d'indication signifie expérimental.
- Les sorties générées (`opportunities*.csv`, caches, builds et environnements
  virtuels) restent hors de Git.
- Les fichiers à la racine sont de petits exercices ou leurs résultats
  pédagogiques ; les nouvelles applications doivent être placées dans un dossier
  nommé et documenté.
- Chaque projet doit documenter son point d'entrée et ses dépendances localement.

## Exécution

Créez un environnement virtuel dans le dossier du projet concerné, puis
installez ses dépendances :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Tous les projets ne possèdent pas encore un fichier `requirements.txt`.
Reportez-vous au README ou aux imports du dossier sélectionné.

## Licence

Sauf mention différente dans un sous-dossier, cette collection est distribuée
sous licence MIT. Certains jeux de données, documents ou médias peuvent rester
soumis à leurs propres conditions.
