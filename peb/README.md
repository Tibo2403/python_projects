# peb

Ce package propose une evaluation simplifiee de la performance energetique des batiments (PEB). Il regroupe plusieurs modules permettant de modeller un batiment, de definir des parametres regionaux et d'obtenir un certificat tres basique.

## Modules

- **models** – Definitions des dataclasses representant murs, fenetres, systeme de chauffage et batiment.
- **config** – Configuration regionale utilisee pour les calculs (degre-jours, facteurs de conversion, etc.).
- **calculations** – Fonctions de calcul des besoins et de l'energie primaire ainsi qu'un score par metre carre.
- **export** – Creation d'un petit certificat PDF/XML (necessite la dependance `fpdf`).
- **examples** – Contient un script d'exemple montrant comment utiliser les modules precedents.

## Utilisation

Executer le script d'exemple :

```bash
python -m peb.examples.usage
```

Lancer les tests unitaires :

```bash
python -m unittest discover -v peb/tests
```

> **Note :** l'export PDF requiert l'installation de la bibliotheque `fpdf`.
