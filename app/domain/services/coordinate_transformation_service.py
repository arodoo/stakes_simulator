"""Coordinate transformation domain service."""

from ..value_objects.coordinate import Coordinate
from ..entities.coordinate_modification import CoordinateModification


class CoordinateTransformationService:
    """Domain service for coordinate transformations and modifications."""
    
    @staticmethod
    def apply_modification(
        original_coordinate: Coordinate, 
        modification: CoordinateModification
    ) -> Coordinate:
        """Apply a coordinate modification to get the final coordinate."""
        if modification.original_coordinate != original_coordinate:
            raise ValueError("Modification original coordinate does not match input")
        
        return modification.modified_coordinate
    
    @staticmethod
    def create_modification(
        record_index: int,
        view,  # ViewType
        original_coordinate: Coordinate,
        new_coordinate: Coordinate
    ) -> CoordinateModification:
        """Create a new coordinate modification."""
        return CoordinateModification(
            record_index=record_index,
            view=view,
            original_coordinate=original_coordinate,
            modified_coordinate=new_coordinate
        )
    
    @staticmethod
    def calculate_delta(
        original: Coordinate, 
        modified: Coordinate
    ) -> Coordinate:
        """Calculate the delta between two coordinates."""
        return Coordinate(
            modified.x - original.x,
            modified.y - original.y
        )
