import unittest

from peb import (
    Building,
    Wall,
    Window,
    HeatingSystem,
    energy_need,
    primary_energy,
    energy_score,
)


class CalculationTests(unittest.TestCase):
    def setUp(self):
        self.building = Building(
            floor_area=120,
            walls=[Wall(area=100, u_value=0.3)],
            windows=[Window(area=20, u_value=1.2)],
            heating=HeatingSystem(efficiency=0.9),
        )
        self.region = "wallonia"

    def test_energy_need(self):
        need = energy_need(self.building, self.region)
        self.assertGreater(need, 0)

    def test_primary_energy(self):
        pe = primary_energy(self.building, self.region)
        self.assertGreater(pe, 0)

    def test_energy_score(self):
        score = energy_score(self.building, self.region)
        self.assertGreater(score, 0)

    def test_infiltration_effect(self):
        b_no_inf = Building(
            floor_area=120,
            walls=[Wall(area=100, u_value=0.3)],
            windows=[Window(area=20, u_value=1.2)],
            heating=HeatingSystem(efficiency=0.9),
            infiltration_rate=0.0,
        )
        base = energy_need(b_no_inf, self.region)

        b_high_inf = Building(
            floor_area=120,
            walls=[Wall(area=100, u_value=0.3)],
            windows=[Window(area=20, u_value=1.2)],
            heating=HeatingSystem(efficiency=0.9),
            infiltration_rate=1.2,
        )
        high = energy_need(b_high_inf, self.region)

        self.assertGreater(high, base)


if __name__ == "__main__":
    unittest.main()
