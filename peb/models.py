"""Data models for building energy performance."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Wall:
    """External wall of a building."""

    area: float  # m^2
    u_value: float  # W/(m^2 K)


@dataclass
class Window:
    """Window of a building."""

    area: float  # m^2
    u_value: float  # W/(m^2 K)


@dataclass
class HeatingSystem:
    """Simple heating system representation."""

    efficiency: float  # between 0 and 1


@dataclass
class Building:
    """Simplified building model."""

    floor_area: float  # m^2 of conditioned floor area
    infiltration_rate: float = 0.6  # air changes per hour
    walls: List[Wall] = field(default_factory=list)
    windows: List[Window] = field(default_factory=list)
    heating: HeatingSystem = field(
        default_factory=lambda: HeatingSystem(efficiency=0.9)
    )

    @property
    def area(self) -> float:
        """Total area of opaque and glazed surfaces."""
        return sum(w.area for w in self.walls) + sum(w.area for w in self.windows)
