"""PEB package implementing a simplified building energy assessment."""

from .models import Building, Wall, Window, HeatingSystem
from .config import REGIONAL_CONFIG
from .calculations import (
    energy_need,
    primary_energy,
    energy_score,
)
try:
    from .export import export_certificate
except Exception:  # pragma: no cover - optional dependency
    export_certificate = None

__all__ = [
    "Building",
    "Wall",
    "Window",
    "HeatingSystem",
    "REGIONAL_CONFIG",
    "energy_need",
    "primary_energy",
    "energy_score",
    "export_certificate",
]
