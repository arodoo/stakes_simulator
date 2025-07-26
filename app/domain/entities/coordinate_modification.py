"""Coordinate modification entity."""

from dataclasses import dataclass
from ..value_objects.coordinate import Coordinate
from ..value_objects.view_type import ViewType


@dataclass
class CoordinateModification:
    """Entity representing a coordinate modification/calibration."""

    record_index: int
    view: ViewType
    original_coordinate: Coordinate
    modified_coordinate: Coordinate

    def __post_init__(self) -> None:
        """Validate coordinate modification."""
        if self.record_index < 0:
            raise ValueError("record_index must be non-negative")
        if not isinstance(self.view, ViewType):
            raise TypeError("view must be a ViewType")
        if not isinstance(self.original_coordinate, Coordinate):
            raise TypeError("original_coordinate must be a Coordinate")
        if not isinstance(self.modified_coordinate, Coordinate):
            raise TypeError("modified_coordinate must be a Coordinate")

    @property
    def delta(self) -> Coordinate:
        """Get the delta (difference) between modified and original coordinates."""
        return Coordinate(
            self.modified_coordinate.x - self.original_coordinate.x,
            self.modified_coordinate.y - self.original_coordinate.y,
        )

    def is_significant(self, threshold: float = 1e-9) -> bool:
        """Check if the modification is significant (above threshold)."""
        delta = self.delta
        return abs(delta.x) > threshold or abs(delta.y) > threshold
