"""Calculation routines for PEB."""

from .models import Building
from .config import REGIONAL_CONFIG


DEGREE_DAY_CONSTANT = 0.024  # (kWh/degree day)


def energy_need(building: Building, region: str) -> float:
    """Return annual heating energy need in kWh."""
    cfg = REGIONAL_CONFIG[region]
    dd = cfg["degree_days"]
    wall_window_loss = sum(w.area * w.u_value for w in building.walls)
    wall_window_loss += sum(w.area * w.u_value for w in building.windows)

    loss = wall_window_loss * dd * DEGREE_DAY_CONSTANT

    infiltration_loss = (
        building.infiltration_rate * building.floor_area * dd * DEGREE_DAY_CONSTANT
    )

    return loss + infiltration_loss


def primary_energy(building: Building, region: str) -> float:
    """Convert energy need to primary energy (kWh)."""
    need = energy_need(building, region)
    efficiency = building.heating.efficiency
    cfg = REGIONAL_CONFIG[region]
    return need / efficiency * cfg["conversion_factor"]


def energy_score(building: Building, region: str) -> float:
    """Compute energy score per square meter."""
    pe = primary_energy(building, region)
    return pe / building.area
