# Corporate Finance — calculs Python (chapitres 4 à 18)

Bibliothèque pédagogique en Python pur couvrant les principales méthodes
quantitatives de *Corporate Finance* de Jonathan Berk et Peter DeMarzo.

Ce projet n'est ni un corrigé officiel ni une reproduction des exercices. Les
fonctions sont génériques et les exemples sont originaux. Utilisez les données
de votre édition dans les fonctions correspondantes.

## Démarrage rapide

Depuis la racine du dépôt :

```powershell
python -m corporate_finance_berk.exemples
```

Consultez le **[guide d'utilisation détaillé](GUIDE_UTILISATION.md)** pour les
conventions, le choix des fonctions et des exemples complets par chapitre.
La **[référence des calculs](REFERENCE_CALCULS.md)** indexe chaque méthode, ses
paramètres et son résultat par chapitre.

| Ch. | Thème | Méthodes |
|---:|---|---|
| 4 | Valeur temps | valeur présente/future, annuités, perpétuité, emprunts |
| 5 | Taux | taux effectif, taux forward |
| 6 | Obligations | prix, YTM, duration, convexité, intérêt couru |
| 7 | Investissement | VAN, TRI, MIRR, récupération, profitabilité |
| 8 | Budget d'investissement | flux incrémentaux, amortissement, seuil, FCF |
| 9 | Actions | Gordon, multi-étapes, multiples, distribution totale |
| 10 | Risque/rendement | espérance, variance, covariance, corrélation |
| 11 | Portefeuille/CAPM | variance matricielle, Sharpe, CAPM |
| 12 | Coût du capital | bêta désendetté/réendetté, WACC |
| 13 | Efficience | rendement anormal, CAR |
| 14 | Structure financière | valeur MM, levier, levier fait maison |
| 15 | Dette/fiscalité | boucliers ponctuels, permanents et programmés |
| 16 | Difficultés financières | coûts directs/indirects, agence, compromis |
| 17 | Distribution | ex-dividende, rachats, BPA, richesse |
| 18 | Valorisation avec levier | APV, FTE, FCFF, FCFE, terminale, WACC |

Tous les taux sont décimaux (`0.08` = 8 %) et les flux commencent en date 0.

```powershell
python -m unittest discover -s corporate_finance_berk/tests -v
python -m compileall corporate_finance_berk
```

```python
from corporate_finance_berk.calculs import npv, wacc
taux = wacc(700, 300, 0.11, 0.05, 0.25)
print(npv(taux, [-1_000, 420, 450, 480]))
```

Ces résultats sont pédagogiques et doivent être vérifiés avant toute décision
financière réelle.
