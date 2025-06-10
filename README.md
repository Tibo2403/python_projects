# Python Projects

Ce depot rassemble plusieurs projets et scripts Python varies. Vous y trouverez des exemples allant de la creation d'un chatbot a la generation d'un tableau de bord, en passant par l'analyse de donnees ou encore la programmation reseau. Les dossiers contiennent des projets independants qui peuvent etre explores separement.

## Structure du depot

- **Algorithme** – Scripts illustrant des algorithmes simples comme le tri par selection ou la manipulation de chaines de caracteres.
- **Chatbot** – Quelques essais autour de la generation de reponses avec la bibliotheque `chatterbot` et des exemples de synthese ou reconnaissance vocale.
- **Chimie** – Fonctions et petits programmes sur des notions chimiques (calcul de pH, configuration electronique…).
- **Dashboard** – Exemple minimal d'utilisation de la bibliotheque `cuxfilter` pour creer un tableau de bord interactif.
- **Design Patterns** – Illustrations de certains patrons de conception, par exemple le patron Composite.
- **ETL** – Script de demonstration d'un processus Extract/Transform/Load (attention : dependances manquantes et noms de modules parfois incorrects).
- **Ethical Hacking** – Exemple tres basique d'echanges reseau via sockets (client et serveur).
- **PizzaMama** – Exemple d'application console consommant une API de pizzeria ; voir egalement le projet Django dans `PizzaMamaDjango`.
- **Python Research** – Divers scripts d'analyse de donnees : regression logistique, random forests, reseaux, etc.
- **Questionnaire** – Implementation orientee objet d'un petit questionnaire interactif.
- **Thermo** – Exercices de thermodynamique (methode d'Euler, capacites thermiques…).
- **api** – Quelques appels d'API simples, dont un exemple pour recuperer les pizzas du projet PizzaMama.
- **kivy** – Mini-projet demontrant la creation d'une fenetre avec Kivy.
- **scraping** – Scripts de web scraping illustrant l'utilisation de `BeautifulSoup`, `requests` ou encore `urllib`.
- **scripting** – Divers exemples de scripts (envoi d'emails, manipulation de fichiers, etc.).
- **youtube downloader** – Programme de telechargement de videos Youtube a l'aide de `pytube` et `ffmpeg`.

De nombreux fichiers annexes (PDF, images, base de donnees, etc.) se trouvent aussi a la racine ou dans certains dossiers.

## Pre-requis

Certains projets necessitent des bibliotheques externes : `chatterbot`, `kivy`, `pytube`, `ffmpeg`, `pandas`, `scikit-learn`, etc. Pensez a creer un environnement virtuel et a installer les dependances necessaires avant d'executer un script particulier.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt  # fichier a creer selon vos besoins
```

## Execution

Chaque dossier contient generalement un ou plusieurs fichiers `main.py` ou equivalents. Reportez-vous au code pour connaitre le point d'entree :

```bash
cd dossier
python fichier.py
```

Certains projets (comme `PizzaMamaDjango`) sont des projets Django complets : il faudra donc appliquer la procedure classique (`python manage.py runserver`).

## Licence

Ce depot est fourni a titre d'exemple pedagogique et n'impose pas de licence particuliere. Vous etes libre de l'etudier et de l'adapter selon vos besoins.

