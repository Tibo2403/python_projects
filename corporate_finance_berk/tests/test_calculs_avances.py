import unittest

from corporate_finance_berk import calculs_avances as c


class TestCalculsAvances(unittest.TestCase):
    def test_ch04_annuites_et_emprunt(self):
        self.assertAlmostEqual(c.annuity_future_value(100, 0.10, 3), 331)
        self.assertAlmostEqual(c.growing_annuity_present_value(100, 0.08, 0.03, 5), 422.0350885)
        payment = c.loan_payment(200_000, 0.06, 20, 12)
        self.assertAlmostEqual(c.remaining_loan_balance(200_000, 0.06, 20, 20, 12), 0)
        self.assertGreater(payment, 0)

    def test_ch05_taux_continu_et_spot(self):
        self.assertAlmostEqual(c.continuous_future_value(100, 0.05, 2), 110.5170918)
        self.assertAlmostEqual(c.continuous_rate_from_ear(0.10), 0.09531018)
        self.assertAlmostEqual(c.spot_rate_from_discount_factor(1 / 1.1**2, 2), 0.10)

    def test_ch06_obligations(self):
        flows = c.bond_cash_flows(1000, 0.06, 2, 2)
        self.assertEqual(flows, [30, 30, 30, 1030])
        self.assertGreater(c.macaulay_duration(1000, 0.06, 0.05, 5, 2), 0)
        self.assertGreater(c.bond_convexity(1000, 0.06, 0.05, 5, 2), 0)
        self.assertEqual(c.dirty_bond_price(980, 50, 90, 180), 1005)

    def test_ch07_criteres(self):
        self.assertAlmostEqual(c.profitability_index(0.10, [600, 600], 1000), 1.0413223)
        self.assertIsNotNone(c.discounted_payback_period(0.05, [-1000, 600, 600]))
        self.assertAlmostEqual(c.modified_irr([-1000, 600, 600], 0.08, 0.10), 0.122497216)

    def test_ch08_flux_incrementaux(self):
        self.assertEqual(c.straight_line_depreciation(1000, 100, 3), 300)
        self.assertEqual(c.incremental_free_cash_flow(1000, 400, 100, 80, 20, 0.25), 375)
        self.assertEqual(c.accounting_break_even(300, 100, 10, 6), 100)

    def test_ch09_multiples_et_payout(self):
        ev = c.enterprise_value_from_ebitda(100, 8)
        self.assertEqual(c.equity_value_from_enterprise_value(ev, 300, 50), 550)
        self.assertEqual(c.price_earnings_value(4, 12), 48)
        self.assertEqual(c.total_payout_model(10_000, 0.10, 0.05, 1000), 200)

    def test_ch10_risque(self):
        self.assertAlmostEqual(c.standard_deviation([0.1, 0.2]), 0.05)
        self.assertAlmostEqual(c.correlation([1, 2, 3], [2, 4, 6]), 1)
        self.assertAlmostEqual(c.geometric_average_return([0.10, -0.10]), (0.99 ** 0.5) - 1)

    def test_ch11_portefeuille(self):
        matrix = [[0.04, 0.006], [0.006, 0.01]]
        self.assertAlmostEqual(c.portfolio_variance([0.5, 0.5], matrix), 0.0155)
        self.assertEqual(c.sharpe_ratio(0.10, 0.02, 0.16), 0.5)

    def test_ch12_13_beta_modele_marche(self):
        beta_a = c.unlevered_beta(1.2, 0.2, 40, 60)
        self.assertAlmostEqual(c.relever_beta(beta_a, 0.2, 40 / 60), 1.2)
        alpha, beta = c.market_model([0.03, 0.05, 0.07], [0.01, 0.02, 0.03])
        self.assertAlmostEqual(alpha, 0.01)
        self.assertAlmostEqual(beta, 2)

    def test_ch14_16_structure_et_dette(self):
        self.assertEqual(c.mm_firm_value(600, 400), 1000)
        self.assertAlmostEqual(c.homemade_leverage_return(0.10, 50, 50, 0.04), 0.16)
        self.assertAlmostEqual(c.pv_tax_shield_schedule([20, 20], 0.25, 0.10), 8.677686, 5)
        distress = c.expected_bankruptcy_cost(0.10, 100, 50)
        self.assertEqual(c.levered_firm_value(1000, 100, distress), 1085)

    def test_ch17_distribution(self):
        self.assertEqual(c.eps_after_repurchase(100, 100, 200, 20), 100 / 90)
        self.assertEqual(c.shareholder_wealth_after_dividend(10, 48, 2), 500)

    def test_ch18_valorisation(self):
        self.assertEqual(c.terminal_value_gordon(10, 0.10, 0.05), 200)
        self.assertEqual(c.fcff(100, 0.25, 20, 30, 5), 60)
        self.assertEqual(c.fcfe(70, 20, 30, 5, 10), 65)
        self.assertGreater(c.enterprise_value_from_fcff([60, 70], 0.10, 200), 0)

    def test_validations(self):
        with self.assertRaises(ValueError):
            c.sharpe_ratio(0.10, 0.02, 0)
        with self.assertRaises(ValueError):
            c.portfolio_variance([1], [[1, 2]])


if __name__ == "__main__":
    unittest.main()
