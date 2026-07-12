# Corporate Finance — calculs Python (chapitres 4 à 18)

Bibliothèque pédagogique en Python pur couvrant les principales méthodes
quantitatives de *Corporate Finance* de Jonathan Berk et Peter DeMarzo.

Ce projet n'est ni un corrigé officiel ni une reproduction des exercices. Les
fonctions sont génériques et les exemples sont originaux. Utilisez les données
de votre édition dans les fonctions correspondantes.

| Ch. | Thème | Méthodes |
|---:|---|---|
| 4 | Valeur temps | valeur présente/future, annuité, perpétuité |
| 5 | Taux | taux effectif, taux forward |
| 6 | Obligations | prix, rendement à maturité |
| 7 | Investissement | VAN, TRI, délai de récupération |
| 8 | Budget d'investissement | flux opérationnel, FCF, annuité équivalente |
| 9 | Actions | Gordon, valorisation multi-étapes |
| 10 | Risque/rendement | espérance, variance |
| 11 | Portefeuille/CAPM | rendement, variance, CAPM |
| 12 | Coût du capital | bêta, WACC |
| 13 | Efficience | rendement anormal, CAR |
| 14 | Structure financière | levier, M&M II |
| 15 | Dette/fiscalité | bouclier fiscal |
| 16 | Difficultés financières | coût attendu de détresse |
| 17 | Distribution | ex-dividende, rachats |
| 18 | Valorisation avec levier | APV, FTE, WACC projet |

Tous les taux sont décimaux (`0.08` = 8 %) et les flux commencent en date 0.

```powershell
python -m corporate_finance_berk.exemples
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
