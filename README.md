# Python Projects

Collection d'exemples, d'exercices et de projets Python. Les applications qui
ont leur propre cycle de publication vivent dans des dépôts autonomes afin
d'éviter les copies divergentes.

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

## Projets autonomes

Les projets suivants ont été extraits dans leur propre dépôt. Leur dépôt
autonome est l'unique source de vérité :

- [`agent_writer_essay`](https://github.com/Tibo2403/agent_writer_essay)
- [`github_project_agent`](https://github.com/Tibo2403/github_project_agent)
- [`price_arbitrage_tool`](https://github.com/Tibo2403/price_arbitrage_tool)

## Conventions d'organisation

- Un projet publié et maintenu indépendamment ne doit pas être recopié ici.
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

Cette collection est fournie à des fins pédagogiques. Les projets disposant
d'une licence propre l'indiquent dans leur dossier.
