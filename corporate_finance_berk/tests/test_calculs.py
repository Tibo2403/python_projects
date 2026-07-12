import unittest
from corporate_finance_berk import calculs as c


class TestChapitres4A18(unittest.TestCase):
    def test_ch04(self): self.assertAlmostEqual(c.present_value(c.future_value(1000,.08,4),.08,4),1000)
    def test_ch05(self): self.assertAlmostEqual(c.effective_annual_rate(.12,12),1.01**12-1)
    def test_ch06(self):
        p=c.bond_price(1000,.05,.06,5,2); self.assertAlmostEqual(c.yield_to_maturity(p,1000,.05,5,2),.06)
    def test_ch07(self):
        f=[-1000,600,600]; self.assertAlmostEqual(c.npv(.1,f),41.322314,5); self.assertAlmostEqual(c.npv(c.irr(f),f),0,7)
    def test_ch08(self): self.assertEqual(c.free_cash_flow(c.operating_cash_flow(1000,500,100,.25),80,20),300)
    def test_ch09(self): self.assertEqual(c.dividend_discount_model(2,.10,.05),40)
    def test_ch10(self): self.assertAlmostEqual(c.expected_return([.1,.2],[.4,.6]),.16)
    def test_ch11(self): self.assertAlmostEqual(c.capm_expected_return(.03,1.2,.08),.09)
    def test_ch12(self): self.assertAlmostEqual(c.wacc(600,400,.10,.05,.25),.075)
    def test_ch13(self): self.assertAlmostEqual(c.cumulative_abnormal_return(c.event_study_abnormal_returns([.02,.05],[.01,.02],1.5)),.025)
    def test_ch14(self): self.assertAlmostEqual(c.mm_levered_equity_cost(.10,.04,.5),.13)
    def test_ch15(self): self.assertEqual(c.levered_value_with_taxes(1000,400,.25),1100)
    def test_ch16(self): self.assertEqual(c.levered_value_with_distress(1000,100,c.expected_distress_cost(.1,500)),1050)
    def test_ch17(self): self.assertEqual(c.shares_after_repurchase(100,1000,20),50)
    def test_ch18(self): self.assertAlmostEqual(c.flow_to_equity([-500,300,300],.10),20.661157,5)


if __name__ == "__main__": unittest.main()
