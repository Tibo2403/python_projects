"""Finance d'entreprise en Python pur. Taux decimaux : 8 % = 0.08."""
from math import isclose
from statistics import fmean


def _list(xs, name="valeurs"):
    xs = [float(x) for x in xs]
    if not xs:
        raise ValueError(f"{name} ne peut pas etre vide")
    return xs


def _rate(r):
    if r <= -1:
        raise ValueError("le taux doit etre superieur a -100 %")
    return float(r)


# Ch. 4 : valeur temps de l'argent
def future_value(pv, rate, periods): return pv * (1 + _rate(rate)) ** periods
def present_value(fv, rate, periods): return fv / (1 + _rate(rate)) ** periods


def annuity_present_value(payment, rate, periods, due=False):
    if periods < 0: raise ValueError("periods doit etre positif")
    value = payment * periods if isclose(rate, 0) else payment * (1 - (1 + _rate(rate)) ** -periods) / rate
    return value * (1 + rate) if due else value


def perpetuity_present_value(payment, rate, growth=0):
    if rate <= growth: raise ValueError("le taux doit depasser la croissance")
    return payment / (rate - growth)


# Ch. 5 : taux d'interet
def effective_annual_rate(apr, compounds_per_year):
    if compounds_per_year <= 0: raise ValueError("frequence invalide")
    return (1 + apr / compounds_per_year) ** compounds_per_year - 1


def forward_rate(spot_short, spot_long, short_years, long_years):
    if not 0 <= short_years < long_years: raise ValueError("maturites invalides")
    return ((1 + spot_long) ** long_years / (1 + spot_short) ** short_years) ** (1 / (long_years - short_years)) - 1


# Ch. 6 : obligations
def bond_price(face, coupon_rate, yield_rate, years, frequency=1):
    periods = round(years * frequency)
    if frequency <= 0 or periods < 1: raise ValueError("frequence ou maturite invalide")
    coupon, y = face * coupon_rate / frequency, yield_rate / frequency
    return annuity_present_value(coupon, y, periods) + present_value(face, y, periods)


def yield_to_maturity(price, face, coupon_rate, years, frequency=1):
    low, high = -.99 * frequency, 10.0
    for _ in range(200):
        mid = (low + high) / 2
        if bond_price(face, coupon_rate, mid, years, frequency) > price: low = mid
        else: high = mid
    return (low + high) / 2


# Ch. 7 : decisions d'investissement
def npv(rate, cash_flows):
    return sum(cf / (1 + _rate(rate)) ** t for t, cf in enumerate(_list(cash_flows, "cash_flows")))


def irr(cash_flows, low=-.999, high=10):
    flows, f_low = _list(cash_flows, "cash_flows"), npv(low, cash_flows)
    if f_low * npv(high, flows) > 0: raise ValueError("aucun TRI unique encadre")
    for _ in range(250):
        mid, f_mid = (low + high) / 2, npv((low + high) / 2, flows)
        if f_low * f_mid <= 0: high = mid
        else: low, f_low = mid, f_mid
    return (low + high) / 2


def payback_period(cash_flows):
    flows, total = _list(cash_flows, "cash_flows"), 0
    for t, flow in enumerate(flows):
        before, total = total, total + flow
        if total >= 0: return 0.0 if t == 0 else t - 1 + (-before / flow if flow else 0)
    return None


# Ch. 8 : budget d'investissement
def operating_cash_flow(revenue, costs, depreciation, tax_rate): return (revenue - costs - depreciation) * (1 - tax_rate) + depreciation
def free_cash_flow(operating_cf, capital_expenditure, change_nwc): return operating_cf - capital_expenditure - change_nwc
def equivalent_annual_annuity(project_npv, rate, periods): return project_npv / annuity_present_value(1, rate, periods)


# Ch. 9 : actions
def dividend_discount_model(next_dividend, required_return, growth): return perpetuity_present_value(next_dividend, required_return, growth)
def stock_price_multistage(dividends, terminal_price, required_return):
    ds = _list(dividends, "dividends")
    return sum(present_value(d, required_return, t) for t, d in enumerate(ds, 1)) + present_value(terminal_price, required_return, len(ds))


# Ch. 10 : risque et rendement
def expected_return(returns, probabilities=None):
    rs = _list(returns, "returns")
    if probabilities is None: return fmean(rs)
    ps = _list(probabilities, "probabilities")
    if len(rs) != len(ps) or not isclose(sum(ps), 1, abs_tol=1e-9): raise ValueError("probabilites invalides")
    return sum(r * p for r, p in zip(rs, ps))


def variance(returns, probabilities=None):
    rs = _list(returns, "returns")
    ps = [1 / len(rs)] * len(rs) if probabilities is None else _list(probabilities, "probabilities")
    mean = expected_return(rs, ps)
    return sum(p * (r - mean) ** 2 for r, p in zip(rs, ps))


# Ch. 11 : portefeuille et CAPM
def portfolio_return(weights, returns):
    ws, rs = _list(weights, "weights"), _list(returns, "returns")
    if len(ws) != len(rs) or not isclose(sum(ws), 1, abs_tol=1e-9): raise ValueError("poids invalides")
    return sum(w * r for w, r in zip(ws, rs))


def two_asset_portfolio_variance(weight_a, sigma_a, sigma_b, correlation):
    b = 1 - weight_a
    return weight_a**2 * sigma_a**2 + b**2 * sigma_b**2 + 2 * weight_a * b * correlation * sigma_a * sigma_b


def capm_expected_return(risk_free, beta, market_return): return risk_free + beta * (market_return - risk_free)


# Ch. 12 : cout du capital
def beta_from_returns(asset_returns, market_returns):
    a, m = _list(asset_returns), _list(market_returns)
    if len(a) != len(m): raise ValueError("series de tailles differentes")
    am, mm = fmean(a), fmean(m)
    cov = sum((x - am) * (y - mm) for x, y in zip(a, m)) / len(a)
    var_m = sum((y - mm) ** 2 for y in m) / len(m)
    if isclose(var_m, 0): raise ValueError("variance du marche nulle")
    return cov / var_m


def wacc(equity, debt, cost_equity, cost_debt, tax_rate):
    total = equity + debt
    if total <= 0: raise ValueError("financement total invalide")
    return equity / total * cost_equity + debt / total * cost_debt * (1 - tax_rate)


# Ch. 13 : efficience des marches
def event_study_abnormal_returns(stock_returns, market_returns, beta=1, alpha=0):
    s, m = _list(stock_returns), _list(market_returns)
    if len(s) != len(m): raise ValueError("series de tailles differentes")
    return [x - (alpha + beta * y) for x, y in zip(s, m)]
def cumulative_abnormal_return(abnormal_returns): return sum(_list(abnormal_returns))


# Ch. 14 : structure financiere en marche parfait
def levered_equity_return(ebit_return, debt_to_equity, debt_return): return ebit_return + debt_to_equity * (ebit_return - debt_return)
def mm_levered_equity_cost(unlevered_cost, debt_cost, debt_to_equity): return unlevered_cost + debt_to_equity * (unlevered_cost - debt_cost)


# Ch. 15 : dette et fiscalite
def interest_tax_shield(interest_expense, tax_rate): return interest_expense * tax_rate
def pv_permanent_tax_shield(debt, tax_rate): return debt * tax_rate
def levered_value_with_taxes(unlevered_value, debt, tax_rate): return unlevered_value + pv_permanent_tax_shield(debt, tax_rate)


# Ch. 16 : difficultes financieres
def expected_distress_cost(probability, distress_cost, discount_rate=0, periods=0):
    if not 0 <= probability <= 1: raise ValueError("probabilite invalide")
    return present_value(probability * distress_cost, discount_rate, periods)
def levered_value_with_distress(unlevered_value, pv_tax_shield, pv_distress_cost): return unlevered_value + pv_tax_shield - pv_distress_cost


# Ch. 17 : politique de distribution
def ex_dividend_price(price_before, dividend, dividend_tax_rate=0, capital_gains_tax_rate=0):
    if capital_gains_tax_rate >= 1: raise ValueError("taux fiscal invalide")
    return price_before - dividend * (1 - dividend_tax_rate) / (1 - capital_gains_tax_rate)


def shares_after_repurchase(shares, cash_used, repurchase_price):
    if repurchase_price <= 0: raise ValueError("prix invalide")
    result = shares - cash_used / repurchase_price
    if result < 0: raise ValueError("rachat excessif")
    return result


# Ch. 18 : valorisation avec levier
def apv(unlevered_cash_flows, unlevered_rate, financing_effects, financing_rate): return npv(unlevered_rate, unlevered_cash_flows) + npv(financing_rate, financing_effects)
def flow_to_equity(equity_cash_flows, cost_equity): return npv(cost_equity, equity_cash_flows)
def wacc_project_value(free_cash_flows, project_wacc): return npv(project_wacc, free_cash_flows)
