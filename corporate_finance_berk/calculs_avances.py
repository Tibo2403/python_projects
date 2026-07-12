"""Calculs complémentaires de finance d'entreprise, chapitres 4 à 18.

Les taux sont décimaux (8 % = 0.08) et les flux commencent en date 0.
Chaque fonction possède une docstring utilisable avec ``help(fonction)``.
"""
from math import exp, isclose, log, sqrt

from .calculs import annuity_present_value, npv, present_value


def _values(values, name="valeurs"):
    result = [float(value) for value in values]
    if not result:
        raise ValueError(f"{name} ne peut pas être vide")
    return result


def _probability(value, name="probabilité"):
    if not 0 <= value <= 1:
        raise ValueError(f"{name} doit être comprise entre 0 et 1")
    return float(value)


# Chapitre 4 — valeur temps de l'argent
def annuity_future_value(payment, rate, periods, due=False):
    """Valeur future de paiements constants; ``due=True`` pour début de période."""
    if periods < 0 or rate <= -1:
        raise ValueError("périodes ou taux invalides")
    value = payment * periods if isclose(rate, 0) else payment * ((1 + rate) ** periods - 1) / rate
    return value * (1 + rate) if due else value


def growing_annuity_present_value(first_payment, rate, growth, periods):
    """Valeur actuelle d'une annuité croissante dont le premier flux arrive en t=1."""
    if periods < 0 or rate <= -1 or growth <= -1:
        raise ValueError("paramètres invalides")
    if isclose(rate, growth):
        return first_payment * periods / (1 + rate)
    return first_payment / (rate - growth) * (1 - ((1 + growth) / (1 + rate)) ** periods)


def loan_payment(principal, annual_rate, periods, payments_per_year=12):
    """Paiement périodique constant d'un emprunt amortissable."""
    if principal < 0 or periods <= 0 or payments_per_year <= 0:
        raise ValueError("emprunt, durée ou fréquence invalide")
    periodic_rate = annual_rate / payments_per_year
    return principal / annuity_present_value(1, periodic_rate, periods * payments_per_year)


def remaining_loan_balance(principal, annual_rate, total_periods, paid_periods, payments_per_year=12):
    """Capital restant dû immédiatement après ``paid_periods`` paiements."""
    count = total_periods * payments_per_year
    paid = paid_periods * payments_per_year
    if not 0 <= paid <= count:
        raise ValueError("nombre de paiements invalide")
    payment = loan_payment(principal, annual_rate, total_periods, payments_per_year)
    return annuity_present_value(payment, annual_rate / payments_per_year, count - paid)


# Chapitre 5 — taux d'intérêt
def continuous_future_value(present, continuous_rate, years):
    """Capitalisation continue: PV × exp(r × t)."""
    return present * exp(continuous_rate * years)


def continuous_rate_from_ear(effective_rate):
    """Convertit un taux annuel effectif en taux annuel continu."""
    if effective_rate <= -1:
        raise ValueError("taux invalide")
    return log(1 + effective_rate)


def spot_rate_from_discount_factor(discount_factor, years):
    """Taux spot annuel implicite d'un facteur d'actualisation."""
    if discount_factor <= 0 or years <= 0:
        raise ValueError("facteur ou maturité invalide")
    return discount_factor ** (-1 / years) - 1


# Chapitre 6 — obligations
def bond_cash_flows(face, coupon_rate, years, frequency=1):
    """Liste des flux d'une obligation, du premier coupon au remboursement."""
    periods = round(years * frequency)
    if face <= 0 or frequency <= 0 or periods <= 0:
        raise ValueError("obligation invalide")
    coupon = face * coupon_rate / frequency
    flows = [coupon] * periods
    flows[-1] += face
    return flows


def macaulay_duration(face, coupon_rate, yield_rate, years, frequency=1):
    """Duration de Macaulay, exprimée en années."""
    flows = bond_cash_flows(face, coupon_rate, years, frequency)
    periodic_yield = yield_rate / frequency
    pv_flows = [flow / (1 + periodic_yield) ** period for period, flow in enumerate(flows, 1)]
    price = sum(pv_flows)
    return sum((period / frequency) * pv for period, pv in enumerate(pv_flows, 1)) / price


def modified_duration(face, coupon_rate, yield_rate, years, frequency=1):
    """Duration modifiée; approximation de -ΔP/P pour une variation du taux."""
    return macaulay_duration(face, coupon_rate, yield_rate, years, frequency) / (1 + yield_rate / frequency)


def bond_convexity(face, coupon_rate, yield_rate, years, frequency=1):
    """Convexité d'une obligation avec rendement nominal et fréquence donnée."""
    flows = bond_cash_flows(face, coupon_rate, years, frequency)
    y = yield_rate / frequency
    price = sum(flow / (1 + y) ** t for t, flow in enumerate(flows, 1))
    numerator = sum(t * (t + 1) * flow / (1 + y) ** (t + 2) for t, flow in enumerate(flows, 1))
    return numerator / (price * frequency**2)


def dirty_bond_price(clean_price, annual_coupon, days_since_coupon, days_in_period):
    """Prix plein = prix au pied du coupon + intérêt couru (convention linéaire)."""
    if days_in_period <= 0 or not 0 <= days_since_coupon <= days_in_period:
        raise ValueError("décompte de jours invalide")
    return clean_price + annual_coupon * days_since_coupon / days_in_period


# Chapitres 7 et 8 — investissement et budget d'investissement
def profitability_index(rate, future_cash_flows, initial_investment):
    """Indice de profitabilité = VA des flux futurs / investissement initial positif."""
    if initial_investment <= 0:
        raise ValueError("investissement initial invalide")
    flows = _values(future_cash_flows, "future_cash_flows")
    return sum(present_value(flow, rate, t) for t, flow in enumerate(flows, 1)) / initial_investment


def discounted_payback_period(rate, cash_flows):
    """Délai de récupération avec actualisation; renvoie ``None`` si non atteint."""
    flows = _values(cash_flows, "cash_flows")
    discounted = [flow / (1 + rate) ** t for t, flow in enumerate(flows)]
    total = 0.0
    for t, flow in enumerate(discounted):
        before, total = total, total + flow
        if total >= 0:
            return 0.0 if t == 0 else t - 1 + (-before / flow if flow else 0)
    return None


def modified_irr(cash_flows, finance_rate, reinvestment_rate):
    """TRI modifié avec taux de financement et de réinvestissement distincts."""
    flows = _values(cash_flows, "cash_flows")
    periods = len(flows) - 1
    if periods <= 0:
        raise ValueError("au moins deux flux sont requis")
    pv_negative = sum(flow / (1 + finance_rate) ** t for t, flow in enumerate(flows) if flow < 0)
    fv_positive = sum(flow * (1 + reinvestment_rate) ** (periods - t) for t, flow in enumerate(flows) if flow > 0)
    if pv_negative >= 0 or fv_positive <= 0:
        raise ValueError("flux positifs et négatifs requis")
    return (fv_positive / -pv_negative) ** (1 / periods) - 1


def straight_line_depreciation(cost, salvage_value, life):
    """Dotation annuelle linéaire."""
    if life <= 0 or cost < salvage_value:
        raise ValueError("coût, valeur résiduelle ou durée invalide")
    return (cost - salvage_value) / life


def incremental_earnings(revenue_change, cost_change, depreciation_change, tax_rate):
    """Résultat opérationnel incrémental après impôt."""
    _probability(tax_rate, "taux d'impôt")
    return (revenue_change - cost_change - depreciation_change) * (1 - tax_rate)


def incremental_free_cash_flow(revenue_change, cost_change, depreciation_change, capex, change_nwc, tax_rate):
    """Flux de trésorerie disponible incrémental d'un projet."""
    return incremental_earnings(revenue_change, cost_change, depreciation_change, tax_rate) + depreciation_change - capex - change_nwc


def accounting_break_even(fixed_costs, depreciation, price, variable_cost, tax_rate=0):
    """Volume rendant le résultat net nul; indépendant du taux d'impôt hors cas limites."""
    _probability(tax_rate, "taux d'impôt")
    margin = price - variable_cost
    if margin <= 0:
        raise ValueError("marge unitaire non positive")
    return (fixed_costs + depreciation) / margin


# Chapitre 9 — valorisation des actions
def price_earnings_value(earnings_per_share, comparable_pe):
    """Valeur par action obtenue par multiple cours/bénéfice."""
    return earnings_per_share * comparable_pe


def enterprise_value_from_ebitda(ebitda, ev_to_ebitda):
    """Valeur d'entreprise par multiple EV/EBITDA."""
    return ebitda * ev_to_ebitda


def equity_value_from_enterprise_value(enterprise_value, debt, cash=0):
    """Valeur des fonds propres = EV - dette + trésorerie."""
    return enterprise_value - debt + cash


def total_payout_model(next_total_payout, required_return, growth, shares):
    """Valeur par action à partir des dividendes et rachats totaux futurs."""
    if required_return <= growth or shares <= 0:
        raise ValueError("rendement, croissance ou nombre d'actions invalide")
    return next_total_payout / (required_return - growth) / shares


# Chapitres 10 et 11 — risque, portefeuille et CAPM
def standard_deviation(returns, probabilities=None):
    """Écart-type population de rendements équiprobables ou pondérés."""
    values = _values(returns, "returns")
    if probabilities is None:
        probabilities = [1 / len(values)] * len(values)
    probs = _values(probabilities, "probabilities")
    if len(values) != len(probs) or not isclose(sum(probs), 1, abs_tol=1e-9):
        raise ValueError("probabilités invalides")
    mean = sum(value * probability for value, probability in zip(values, probs))
    return sqrt(sum(probability * (value - mean) ** 2 for value, probability in zip(values, probs)))


def covariance(series_a, series_b):
    """Covariance population de deux séries de même taille."""
    a, b = _values(series_a), _values(series_b)
    if len(a) != len(b):
        raise ValueError("séries de tailles différentes")
    mean_a, mean_b = sum(a) / len(a), sum(b) / len(b)
    return sum((x - mean_a) * (y - mean_b) for x, y in zip(a, b)) / len(a)


def correlation(series_a, series_b):
    """Corrélation de Pearson population."""
    sigma_a, sigma_b = standard_deviation(series_a), standard_deviation(series_b)
    if isclose(sigma_a * sigma_b, 0):
        raise ValueError("écart-type nul")
    return covariance(series_a, series_b) / (sigma_a * sigma_b)


def geometric_average_return(returns):
    """Rendement moyen géométrique par période."""
    values = _values(returns, "returns")
    product = 1.0
    for value in values:
        if value <= -1:
            raise ValueError("un rendement ne peut pas être inférieur ou égal à -100 %")
        product *= 1 + value
    return product ** (1 / len(values)) - 1


def portfolio_variance(weights, covariance_matrix):
    """Variance d'un portefeuille: w'Σw."""
    w = _values(weights, "weights")
    matrix = [_values(row, "covariance_matrix") for row in covariance_matrix]
    if len(matrix) != len(w) or any(len(row) != len(w) for row in matrix):
        raise ValueError("dimensions incompatibles")
    return sum(w[i] * w[j] * matrix[i][j] for i in range(len(w)) for j in range(len(w)))


def sharpe_ratio(expected_portfolio_return, risk_free_rate, volatility):
    """Ratio de Sharpe du portefeuille."""
    if volatility <= 0:
        raise ValueError("volatilité non positive")
    return (expected_portfolio_return - risk_free_rate) / volatility


# Chapitres 12 et 13 — coût du capital et modèle de marché
def unlevered_beta(equity_beta, debt_beta, debt, equity):
    """Bêta des actifs comme moyenne pondérée des bêtas dette et fonds propres."""
    if debt + equity <= 0:
        raise ValueError("valeur de financement invalide")
    return equity / (debt + equity) * equity_beta + debt / (debt + equity) * debt_beta


def relever_beta(asset_beta, debt_beta, debt_to_equity):
    """Bêta des fonds propres à partir du bêta des actifs et du levier."""
    return asset_beta + debt_to_equity * (asset_beta - debt_beta)


def market_model(stock_returns, market_returns):
    """Estime (alpha, bêta) du modèle de marché par moindres carrés."""
    stocks, market = _values(stock_returns), _values(market_returns)
    if len(stocks) != len(market):
        raise ValueError("séries de tailles différentes")
    beta = covariance(stocks, market) / covariance(market, market)
    alpha = sum(stocks) / len(stocks) - beta * sum(market) / len(market)
    return alpha, beta


# Chapitres 14 à 16 — structure financière, impôts et détresse
def mm_firm_value(equity, debt):
    """Valeur de l'entreprise en marché parfait: E + D."""
    if equity < 0 or debt < 0:
        raise ValueError("valeurs négatives")
    return equity + debt


def homemade_leverage_return(asset_return, borrowing, own_equity, borrowing_rate):
    """Rendement obtenu en reproduisant personnellement un levier financier."""
    if own_equity <= 0:
        raise ValueError("apport personnel non positif")
    return ((own_equity + borrowing) * (1 + asset_return) - borrowing * (1 + borrowing_rate)) / own_equity - 1


def pv_tax_shield_schedule(interest_payments, tax_rate, discount_rate):
    """VA d'une série de boucliers fiscaux d'intérêts à partir de t=1."""
    _probability(tax_rate, "taux d'impôt")
    payments = _values(interest_payments, "interest_payments")
    return sum(present_value(payment * tax_rate, discount_rate, t) for t, payment in enumerate(payments, 1))


def expected_bankruptcy_cost(probability, direct_cost, indirect_cost=0, discount_rate=0, years=0):
    """VA du coût attendu de faillite, direct et indirect."""
    _probability(probability)
    return present_value(probability * (direct_cost + indirect_cost), discount_rate, years)


def levered_firm_value(unlevered_value, tax_shield_value=0, distress_cost_value=0, agency_effect_value=0):
    """Valeur avec dette: VU + bouclier - détresse + effet net d'agence."""
    return unlevered_value + tax_shield_value - distress_cost_value + agency_effect_value


# Chapitre 17 — politique de distribution
def eps_after_repurchase(net_income, shares, cash_used, repurchase_price, lost_after_tax_interest=0):
    """BPA après rachat, en retranchant le revenu après impôt perdu sur la trésorerie."""
    remaining = shares - cash_used / repurchase_price
    if remaining <= 0:
        raise ValueError("rachat excessif")
    return (net_income - lost_after_tax_interest) / remaining


def shareholder_wealth_after_dividend(shares, ex_dividend_price, dividend_per_share):
    """Richesse brute après distribution: valeur des actions + dividende reçu."""
    return shares * (ex_dividend_price + dividend_per_share)


# Chapitre 18 — valorisation avec levier
def terminal_value_gordon(next_cash_flow, discount_rate, growth):
    """Valeur terminale de Gordon à la date précédant ``next_cash_flow``."""
    if discount_rate <= growth:
        raise ValueError("le taux d'actualisation doit dépasser la croissance")
    return next_cash_flow / (discount_rate - growth)


def fcff(ebit, tax_rate, depreciation, capital_expenditure, change_nwc):
    """Flux disponible pour dette et fonds propres: EBIT(1-T)+D&A-CapEx-ΔBFR."""
    _probability(tax_rate, "taux d'impôt")
    return ebit * (1 - tax_rate) + depreciation - capital_expenditure - change_nwc


def fcfe(net_income, depreciation, capital_expenditure, change_nwc, net_borrowing):
    """Flux disponible pour les actionnaires."""
    return net_income + depreciation - capital_expenditure - change_nwc + net_borrowing


def enterprise_value_from_fcff(free_cash_flows, wacc, terminal_value=0):
    """Valeur d'entreprise: VA des FCFF de t=1 à N et valeur terminale en N."""
    flows = _values(free_cash_flows, "free_cash_flows")
    return sum(present_value(flow, wacc, t) for t, flow in enumerate(flows, 1)) + present_value(terminal_value, wacc, len(flows))


def equity_value_from_fcfe(equity_cash_flows, cost_equity, terminal_value=0):
    """Valeur des fonds propres: VA des FCFE de t=1 à N et terminale en N."""
    flows = _values(equity_cash_flows, "equity_cash_flows")
    return sum(present_value(flow, cost_equity, t) for t, flow in enumerate(flows, 1)) + present_value(terminal_value, cost_equity, len(flows))
