# Design Patterns

Ce dossier presente plusieurs patrons de conception classiques en Python. Les fichiers associes montrent une implementation tres simplifiee pour illustrer l'idee generale.

## Quand utiliser ces patterns ?

| Pattern    | Quand l'utiliser                                                |
|------------|----------------------------------------------------------------|
| Singleton  | Lorsqu'une seule instance d'une classe doit exister et etre partagee dans tout le programme. |
| Factory    | Quand la creation d'objets doit etre decouplee de leur utilisation. Utile pour retourner des sous-classes specifiques sans exposer la logique de creation. |
| Observer   | Pour notifier plusieurs objets (observers) qu'un evenement s'est produit dans un autre objet (subject) sans couplage fort. |
| Strategy   | Quand plusieurs algorithmes sont interchangeables a l'execution. Le contexte peut changer la strategie au vol. |
| Composite  | Pour manipuler de maniere uniforme des objets simples et des compositions d'objets. |
| Decorator  | Pour ajouter dynamiquement des fonctionnalites a un objet sans modifier son code d'origine. |
| Adapter    | Pour adapter l'interface d'un objet a celle attendue par le client. |

## Comment les mettre en oeuvre ?

- **Singleton** : utiliser un metaclasse ou une variable de classe stockant l'instance unique. Voir `Singleton.py`.
- **Factory** : creer une classe ou une fonction chargee de retourner des objets de type approprie selon un parametre. Voir `Factory.py`.
- **Observer** : definir un `Subject` qui conserve une liste d'observateurs et les notifie via une methode commune (`update`). Voir `Observer.py`.
- **Strategy** : definir plusieurs fonctions ou classes encapsulant des algorithmes; le `Context` possede une reference a la strategie et la delegue. Voir `Strategy.py`.
- **Composite** : chaque objet de la composition possede la meme interface que les objets simples pour pouvoir les traiter de la meme maniere. Voir `Composite.py`.
- **Decorator** : envelopper un objet pour lui ajouter des comportements au moment de l'execution sans toucher a son code. Voir `Decorator.py`.
- **Adapter** : encapsuler un objet pour presenter l'interface qu'attend le client. Voir `Adapter.py`.
