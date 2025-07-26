"""Vehicle record entity."""

from dataclasses import dataclass
from typing import Dict, Optional
from ..value_objects.coordinate import Coordinate
from ..value_objects.view_type import ViewType


@dataclass
class VehicleRecord:
    """Entity representing a vehicle record with coordinates across different views."""
    
    record_id: int
    mag_id: int
    coordinates: Dict[str, Coordinate]
    
    def __post_init__(self) -> None:
        """Validate vehicle record."""
        if self.record_id < 0:
            raise ValueError("record_id must be non-negative")
        if not isinstance(self.coordinates, dict):
            raise TypeError("coordinates must be a dictionary")
    
    def get_coordinate(self, view: ViewType) -> Optional[Coordinate]:
        """Get coordinate for a specific view."""
        return self.coordinates.get(view.value)
    
    def set_coordinate(self, view: ViewType, coordinate: Coordinate) -> None:
        """Set coordinate for a specific view."""
        self.coordinates[view.value] = coordinate
    
    def has_coordinate(self, view: ViewType) -> bool:
        """Check if record has coordinate for a specific view."""
        return view.value in self.coordinates
