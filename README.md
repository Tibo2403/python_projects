# Python Projects

Ce dépôt rassemble des projets Python indépendants à vocation pédagogique ou expérimentale. Chaque dossier doit être considéré comme un projet autonome : ses dépendances, son point d’entrée et son niveau de maintenance peuvent différer.

## Projets principaux

### Finance d’entreprise

- [`corporate_finance_berk`](corporate_finance_berk/) : calculs pédagogiques en Python pur couvrant les concepts quantitatifs des chapitres 4 à 18 de *Corporate Finance* (Berk et DeMarzo), avec exemples, tests, [guide d’utilisation](corporate_finance_berk/GUIDE_UTILISATION.md) et [référence des calculs](corporate_finance_berk/REFERENCE_CALCULS.md).

### Autres projets et exemples

- **Algorithme** — algorithmes simples et manipulation de chaînes.
- **Chatbot** — essais autour de `chatterbot`, de la synthèse et de la reconnaissance vocale.
- **Chimie** — calculs de pH, configuration électronique et autres exemples.
- **Dashboard** — exemple minimal avec `cuxfilter`.
- **Design Patterns** — Composite, Singleton, Factory, Observer, Strategy, Decorator et Adapter.
- **ETL** — démonstration Extract/Transform/Load ; certaines dépendances doivent encore être normalisées.
- **Ethical Hacking** — exemples réseau élémentaires avec sockets.
- **PizzaMama** et **PizzaMamaDjango** — applications console et Django autour d’une API de pizzeria.
- **Python Research** — scripts d’analyse de données et de machine learning.
- **Questionnaire** — questionnaire interactif orienté objet.
- **Thermo** — exercices de thermodynamique.
- **api** — exemples d’appels API.
- **kivy** — mini-application Kivy.
- **MobilityMap** — application Flask et carte Leaflet.
- **agent_writer_essay** — agent d’écriture avec CLI et interface Gradio.
- **github_project_agent** — agent LangChain pour analyser des projets GitHub.
- **price_arbitrage_tool** — calculateur d’arbitrage à partir de CSV autorisés.
- **scraping** — exemples avec BeautifulSoup, Requests et urllib.
- **scripting** — scripts utilitaires variés.
- **youtube downloader** — exemple utilisant `pytube` et `ffmpeg`.
- **peb** — package de calcul simplifié de performance énergétique du bâtiment.

## Installation

Il n’existe volontairement pas de fichier global `requirements.txt` : les projets n’utilisent pas tous les mêmes bibliothèques ni les mêmes versions.

Créez un environnement virtuel dans le dossier du projet concerné :

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

Installez ensuite les dépendances documentées par ce projet. Évitez d’installer toutes les bibliothèques du dépôt dans un seul environnement.

## Vérifications communes

Les contrôles transversaux restent volontairement prudents pour ne pas casser les exemples historiques :

```bash
python -m pip install ruff pytest
python -m compileall -q .
ruff check . --select E9,F63,F7,F82
pytest
```

La CI exécute ces commandes sur chaque pull request. Les règles plus strictes doivent être activées progressivement, projet par projet.

## Règles de maintenance

Pour toute nouvelle contribution :

1. Placez le code dans un dossier de projet clairement nommé.
2. Ajoutez un README local avec l’objectif, le point d’entrée et les dépendances.
3. Ajoutez au moins un test pour toute logique métier réutilisable.
4. Ne versionnez pas d’environnement virtuel, de cache, de base locale ni de fichier `.env`.
5. Préférez un petit module cohérent à plusieurs scripts quasi identiques.
6. Indiquez explicitement si un projet est actif, expérimental ou archivé.

## Exécution

Chaque dossier contient généralement un `main.py`, un script principal ou des instructions propres. Exemple :

```bash
cd dossier
python fichier.py
```

Pour Django :

```bash
python manage.py runserver
```

## Licence

Ce dépôt est fourni à titre pédagogique. Vérifiez également les licences des bibliothèques, données et ressources externes utilisées par chaque sous-projet.
