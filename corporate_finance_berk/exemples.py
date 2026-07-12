"""Exemples originaux : python -m corporate_finance_berk.exemples"""
from . import calculs as c


def main():
    examples = {
        "Ch. 4 - valeur future": c.future_value(1000, .06, 5),
        "Ch. 5 - taux effectif": c.effective_annual_rate(.06, 12),
        "Ch. 6 - obligation": c.bond_price(1000, .05, .06, 5),
        "Ch. 7 - VAN": c.npv(.10, [-1000, 450, 450, 450]),
        "Ch. 8 - FCF": c.free_cash_flow(c.operating_cash_flow(800, 420, 80, .25), 90, 20),
        "Ch. 9 - action": c.dividend_discount_model(2.1, .09, .04),
        "Ch. 10 - esperance": c.expected_return([.2, .08, -.1], [.25, .5, .25]),
        "Ch. 11 - CAPM": c.capm_expected_return(.03, 1.2, .09),
        "Ch. 12 - WACC": c.wacc(700, 300, .11, .05, .25),
        "Ch. 13 - CAR": c.cumulative_abnormal_return(c.event_study_abnormal_returns([.03, .05], [.01, .02])),
        "Ch. 14 - cout fonds propres": c.mm_levered_equity_cost(.09, .04, .5),
        "Ch. 15 - bouclier fiscal": c.interest_tax_shield(50, .25),
        "Ch. 16 - cout detresse": c.expected_distress_cost(.08, 500, .06, 3),
        "Ch. 17 - cours ex-dividende": c.ex_dividend_price(50, 2),
        "Ch. 18 - APV": c.apv([-1000, 450, 450, 450], .10, [0, 15, 15, 15], .05),
    }
    for label, value in examples.items(): print(f"{label}: {value:.4f}")


if __name__ == "__main__": main()
