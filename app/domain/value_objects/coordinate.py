"""Coordinate value object."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Coordinate:
    """Immutable coordinate value object."""
    
    x: float
    y: float
    
    def __post_init__(self) -> None:
        """Validate coordinate values."""
        if not isinstance(self.x, (int, float)):
            raise TypeError("x must be a number")
        if not isinstance(self.y, (int, float)):
            raise TypeError("y must be a number")
    
    def add(self, dx: float, dy: float) -> 'Coordinate':
        """Return a new coordinate with the given offset."""
        return Coordinate(self.x + dx, self.y + dy)
    
    def to_tuple(self) -> Tuple[float, float]:
        """Convert to tuple representation."""
        return (self.x, self.y)
    
    @classmethod
    def from_tuple(cls, coord_tuple: Tuple[float, float]) -> 'Coordinate':
        """Create coordinate from tuple."""
        return cls(coord_tuple[0], coord_tuple[1])
    
    def distance_to(self, other: 'Coordinate') -> float:
        """Calculate distance to another coordinate."""
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
