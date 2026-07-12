# Guide d'utilisation

Ce guide explique comment lancer les exemples et utiliser les fonctions de
`corporate_finance_berk` avec vos propres données.

## 1. Prérequis et lancement

Le module fonctionne avec Python 3 et n'utilise aucune bibliothèque externe.
Clonez le dépôt, ouvrez un terminal dans sa racine, puis lancez :

```powershell
git clone https://github.com/Tibo2403/python_projects.git
cd python_projects
python -m corporate_finance_berk.exemples
```

Il n'est pas nécessaire d'exécuter `pip install`. Le terminal doit simplement
être placé à la racine du dépôt afin que Python trouve le package.

Pour utiliser une fonction dans votre propre script :

```python
from corporate_finance_berk.calculs import future_value, npv

capital_dans_5_ans = future_value(10_000, rate=0.06, periods=5)
van_projet = npv(0.10, [-20_000, 8_000, 9_000, 10_000])

print(f"Valeur future : {capital_dans_5_ans:,.2f} €")
print(f"VAN du projet : {van_projet:,.2f} €")
```

## 2. Conventions importantes

- Les taux sont écrits sous forme décimale : `0.08` signifie 8 %, pas 8.
- Les périodes doivent être cohérentes avec le taux. Un taux annuel attend des
  périodes en années ; un taux mensuel attend des périodes en mois.
- Une série de flux commence en date 0. Un investissement initial est donc
  généralement négatif : `[-1000, 400, 450, 500]`.
- Les montants peuvent être exprimés en euros, dollars ou milliers d'euros, à
  condition de conserver la même unité dans tout le calcul.
- Les fonctions renvoient des nombres bruts. Utilisez par exemple
  `f"{resultat:.2f}"` pour afficher deux décimales.
- Les fonctions lèvent `ValueError` lorsqu'un calcul n'est pas défini ou que
  les données sont incohérentes.

## 3. Choisir la bonne fonction

| Besoin | Fonction |
|---|---|
| Capitaliser une somme | `future_value` |
| Actualiser un flux futur | `present_value` |
| Actualiser une annuité ou perpétuité | `annuity_present_value`, `perpetuity_present_value` |
| Convertir un taux nominal en taux effectif | `effective_annual_rate` |
| Calculer le prix ou le rendement d'une obligation | `bond_price`, `yield_to_maturity` |
| Évaluer un projet | `npv`, `irr`, `payback_period` |
| Construire les flux d'un projet | `operating_cash_flow`, `free_cash_flow` |
| Valoriser une action | `dividend_discount_model`, `stock_price_multistage` |
| Mesurer rendement et risque | `expected_return`, `variance` |
| Évaluer un portefeuille ou appliquer le CAPM | `portfolio_return`, `two_asset_portfolio_variance`, `capm_expected_return` |
| Estimer le coût du capital | `beta_from_returns`, `wacc` |
| Étudier une réaction boursière | `event_study_abnormal_returns`, `cumulative_abnormal_return` |
| Mesurer l'effet du levier | `levered_equity_return`, `mm_levered_equity_cost` |
| Calculer le bouclier fiscal | `interest_tax_shield`, `pv_permanent_tax_shield` |
| Intégrer le risque de détresse | `expected_distress_cost`, `levered_value_with_distress` |
| Étudier dividendes et rachats | `ex_dividend_price`, `shares_after_repurchase` |
| Valoriser un projet financé par dette | `apv`, `flow_to_equity`, `wacc_project_value` |

## 4. Exemples par groupe de chapitres

### Chapitres 4 à 6 — actualisation, taux et obligations

```python
from corporate_finance_berk.calculs import (
    annuity_present_value,
    bond_price,
    effective_annual_rate,
)

# Valeur actuelle de 12 paiements annuels de 1 000 € à 5 %.
valeur_annuite = annuity_present_value(1_000, 0.05, 12)

# Taux annuel effectif d'un taux nominal de 6 %, composé mensuellement.
taux_effectif = effective_annual_rate(0.06, 12)

# Obligation : nominal 1 000 €, coupon 5 %, rendement 6 %, maturité 5 ans.
prix_obligation = bond_price(1_000, 0.05, 0.06, 5)
```

Pour une obligation semestrielle, passez `frequency=2`. Les taux de coupon et
de rendement restent annuels ; la fonction effectue la conversion par période.

### Chapitres 7 et 8 — décision et budget d'investissement

```python
from corporate_finance_berk.calculs import free_cash_flow, irr, npv, operating_cash_flow

flux_operationnel = operating_cash_flow(
    revenue=500_000,
    costs=300_000,
    depreciation=40_000,
    tax_rate=0.25,
)
flux_libre = free_cash_flow(
    operating_cf=flux_operationnel,
    capital_expenditure=60_000,
    change_nwc=15_000,
)

flux_projet = [-250_000, 80_000, 95_000, 110_000]
van = npv(0.09, flux_projet)
tri = irr(flux_projet)

decision = "accepter" if van > 0 else "rejeter"
print(f"VAN = {van:,.2f} €, TRI = {tri:.2%} : {decision}")
```

La règle VAN recommande normalement d'accepter un projet si sa VAN est
positive au coût du capital approprié. Le TRI peut être ambigu lorsque les flux
changent plusieurs fois de signe ; dans ce cas, privilégiez la VAN.

### Chapitres 9 à 13 — actions, risque et coût du capital

```python
from corporate_finance_berk.calculs import (
    capm_expected_return,
    dividend_discount_model,
    portfolio_return,
    wacc,
)

prix_action = dividend_discount_model(
    next_dividend=2.50,
    required_return=0.09,
    growth=0.04,
)

rendement_portefeuille = portfolio_return(
    weights=[0.60, 0.40],
    returns=[0.08, 0.13],
)

cout_fonds_propres = capm_expected_return(
    risk_free=0.03,
    beta=1.20,
    market_return=0.09,
)

cout_moyen = wacc(
    equity=700_000,
    debt=300_000,
    cost_equity=cout_fonds_propres,
    cost_debt=0.05,
    tax_rate=0.25,
)
```

Dans le modèle de Gordon, `required_return` doit être strictement supérieur à
`growth`. Pour `portfolio_return`, la somme des poids doit être égale à 1.

### Chapitres 14 à 18 — financement, fiscalité et levier

```python
from corporate_finance_berk.calculs import (
    apv,
    expected_distress_cost,
    levered_value_with_distress,
    pv_permanent_tax_shield,
)

valeur_sans_dette = 1_000_000
dette = 300_000
taux_impot = 0.25

bouclier = pv_permanent_tax_shield(dette, taux_impot)
cout_detresse = expected_distress_cost(
    probability=0.08,
    distress_cost=400_000,
    discount_rate=0.07,
    periods=3,
)
valeur_avec_dette = levered_value_with_distress(
    valeur_sans_dette,
    pv_tax_shield=bouclier,
    pv_distress_cost=cout_detresse,
)

# APV = VAN du projet non endetté + VAN des effets du financement.
valeur_apv = apv(
    unlevered_cash_flows=[-500_000, 210_000, 230_000, 250_000],
    unlevered_rate=0.10,
    financing_effects=[0, 12_000, 10_000, 8_000],
    financing_rate=0.05,
)
```

`financing_effects` commence également en date 0. Il peut contenir les
boucliers fiscaux ou d'autres effets du financement, avec le signe approprié.

## 5. Vérifier vos modifications

Depuis la racine du dépôt :

```powershell
python -m unittest discover -s corporate_finance_berk/tests -v
python -m compileall corporate_finance_berk
```

La première commande exécute les tests couvrant les chapitres 4 à 18. La
seconde vérifie la syntaxe de tous les fichiers Python du module.

## 6. Limites

Cette bibliothèque est un support pédagogique : elle ne remplace pas les
hypothèses, conventions et explications du manuel. Vérifiez notamment la
fréquence des taux, la chronologie des flux, les hypothèses fiscales et le coût
du capital avant d'utiliser un résultat dans une décision réelle.
