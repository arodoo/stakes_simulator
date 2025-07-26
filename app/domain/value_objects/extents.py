"""Extents value object for coordinate bounds."""

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class Extents:
    """Immutable extents value object representing coordinate bounds."""

    min_x: float
    max_x: float
    min_y: float
    max_y: float

    def __post_init__(self) -> None:
        """Validate extents values."""
        if self.min_x > self.max_x:
            raise ValueError("min_x cannot be greater than max_x")
        if self.min_y > self.max_y:
            raise ValueError("min_y cannot be greater than max_y")

    @property
    def x_range(self) -> float:
        """Get the x range (width)."""
        return max(self.max_x - self.min_x, 1e-9)

    @property
    def y_range(self) -> float:
        """Get the y range (height)."""
        return max(self.max_y - self.min_y, 1e-9)

    def to_tuple(self) -> Tuple[float, float, float, float]:
        """Convert to tuple representation."""
        return (self.min_x, self.max_x, self.min_y, self.max_y)

    @classmethod
    def from_tuple(cls, extents_tuple: Tuple[float, float, float, float]) -> "Extents":
        """Create extents from tuple."""
        return cls(
            extents_tuple[0], extents_tuple[1], extents_tuple[2], extents_tuple[3]
        )
