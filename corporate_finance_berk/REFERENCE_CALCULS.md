# Référence des calculs — chapitres 4 à 18

Cette page permet de retrouver une fonction à partir du calcul recherché.
Importez les fonctions historiques depuis `calculs` et les compléments depuis
`calculs_avances` :

```python
from corporate_finance_berk import calculs as base
from corporate_finance_berk import calculs_avances as avance

van = base.npv(0.10, [-1_000, 600, 600])
duration = avance.modified_duration(1_000, 0.05, 0.06, 5, frequency=2)
```

`help(avance.modified_duration)` affiche la documentation intégrée. Les taux
sont décimaux (`0.08` = 8 %) et les flux commencent en date 0.

> Les intitulés varient selon l'édition de *Corporate Finance*. La bibliothèque
> couvre les méthodes quantitatives générales avec des exemples originaux;
> elle ne reproduit ni les exercices ni leur corrigé.

## Catalogue par chapitre

| Ch. | Calcul | Fonction | Résultat / convention |
|---:|---|---|---|
| 4 | valeur future / actuelle | `future_value`, `present_value` | montant à la date cible |
| 4 | VA / VF d'annuité | `annuity_present_value`, `annuity_future_value` | `due=True` = début de période |
| 4 | perpétuité / annuité croissante | `perpetuity_present_value`, `growing_annuity_present_value` | premier flux en t=1 |
| 4 | emprunt amortissable | `loan_payment`, `remaining_loan_balance` | paiement et capital restant dû |
| 5 | taux annuel effectif | `effective_annual_rate` | taux nominal vers effectif |
| 5 | taux forward | `forward_rate` | taux implicite entre deux maturités |
| 5 | capitalisation continue | `continuous_future_value`, `continuous_rate_from_ear` | valeur future / taux continu |
| 5 | taux spot | `spot_rate_from_discount_factor` | taux issu d'un facteur d'actualisation |
| 6 | prix et rendement obligataire | `bond_price`, `yield_to_maturity` | prix plein théorique / YTM |
| 6 | échéancier | `bond_cash_flows` | coupons puis nominal au dernier flux |
| 6 | sensibilité | `macaulay_duration`, `modified_duration`, `bond_convexity` | durée en années, convexité |
| 6 | intérêt couru | `dirty_bond_price` | prix coté + intérêt couru |
| 7 | VAN et TRI | `npv`, `irr` | premier flux en t=0 |
| 7 | récupération | `payback_period`, `discounted_payback_period` | `None` si jamais récupéré |
| 7 | profitabilité / MIRR | `profitability_index`, `modified_irr` | indice / taux modifié |
| 8 | flux opérationnel / FCF | `operating_cash_flow`, `free_cash_flow` | flux après impôt et investissement |
| 8 | flux incrémental | `incremental_earnings`, `incremental_free_cash_flow` | variation liée au projet |
| 8 | amortissement / seuil | `straight_line_depreciation`, `accounting_break_even` | dotation / volume nul |
| 8 | annuité équivalente | `equivalent_annual_annuity` | comparaison de durées différentes |
| 9 | dividendes | `dividend_discount_model`, `stock_price_multistage` | valeur par action |
| 9 | multiples | `price_earnings_value`, `enterprise_value_from_ebitda` | valeur fonds propres / entreprise |
| 9 | passage EV vers equity | `equity_value_from_enterprise_value` | EV - dette + trésorerie |
| 9 | distribution totale | `total_payout_model` | dividendes + rachats par action |
| 10 | rendement et dispersion | `expected_return`, `variance`, `standard_deviation` | moyenne et risque population |
| 10 | dépendance | `covariance`, `correlation` | covariance / Pearson |
| 10 | rendement composé moyen | `geometric_average_return` | moyenne géométrique par période |
| 11 | portefeuille | `portfolio_return`, `portfolio_variance` | rendement / w'Σw |
| 11 | portefeuille à deux actifs | `two_asset_portfolio_variance` | variance avec corrélation |
| 11 | performance / CAPM | `sharpe_ratio`, `capm_expected_return` | Sharpe / rendement requis |
| 12 | bêta historique | `beta_from_returns` | cov(actif,marché)/var(marché) |
| 12 | bêta désendetté / réendetté | `unlevered_beta`, `relever_beta` | risque actif / fonds propres |
| 12 | coût moyen pondéré | `wacc` | coût de dette après impôt |
| 13 | modèle de marché | `market_model` | tuple `(alpha, beta)` |
| 13 | étude d'événement | `event_study_abnormal_returns`, `cumulative_abnormal_return` | AR / CAR |
| 14 | valeur et rendement MM | `mm_firm_value`, `levered_equity_return`, `mm_levered_equity_cost` | E+D / coût des fonds propres |
| 14 | levier fait maison | `homemade_leverage_return` | rendement après emprunt personnel |
| 15 | bouclier fiscal | `interest_tax_shield`, `pv_permanent_tax_shield` | période / dette permanente |
| 15 | échéancier de boucliers | `pv_tax_shield_schedule` | VA des économies fiscales |
| 16 | détresse / faillite | `expected_distress_cost`, `expected_bankruptcy_cost` | coût attendu actualisé |
| 16 | valeur ajustée | `levered_firm_value` | VU + fiscalité - détresse + agence |
| 17 | ex-dividende / rachat | `ex_dividend_price`, `shares_after_repurchase` | prix fiscalisé / actions restantes |
| 17 | BPA / richesse | `eps_after_repurchase`, `shareholder_wealth_after_dividend` | résultat par action / patrimoine |
| 18 | APV / FTE / WACC | `apv`, `flow_to_equity`, `wacc_project_value` | trois méthodes de valorisation |
| 18 | flux disponibles | `fcff`, `fcfe` | flux entreprise / actionnaires |
| 18 | valeur terminale | `terminal_value_gordon` | prochain flux / (r-g) |
| 18 | DCF complet | `enterprise_value_from_fcff`, `equity_value_from_fcfe` | VA des flux t=1..N + terminale |

## Exemples ciblés

```python
from corporate_finance_berk import calculs_avances as c

# Emprunt de 200 000 € à 6 %, sur 20 ans, mensualités constantes.
mensualite = c.loan_payment(200_000, 0.06, 20, 12)

# Sensibilité d'une obligation semestrielle.
duration = c.modified_duration(1_000, 0.05, 0.06, 5, 2)
convexite = c.bond_convexity(1_000, 0.05, 0.06, 5, 2)

# Valorisation DCF par FCFF.
flux = [c.fcff(100, 0.25, 20, 30, 5), 70]
terminale = c.terminal_value_gordon(72, 0.09, 0.03)
valeur_entreprise = c.enterprise_value_from_fcff(flux, 0.09, terminale)
```

Pour une petite variation obligataire `dy`, l'approximation usuelle est
`ΔP/P ≈ -duration_modifiee × dy + 0.5 × convexite × dy²`.

## Vérification et limites

```powershell
python -m unittest discover -s corporate_finance_berk/tests -v
python -m compileall corporate_finance_berk
```

Les résultats sont pédagogiques et ne constituent pas un conseil financier.
Les conventions de jours, règles fiscales, options et données de marché réelles
peuvent demander des hypothèses supplémentaires. Vérifiez les unités, les dates
des flux et les conventions demandées par votre édition.
