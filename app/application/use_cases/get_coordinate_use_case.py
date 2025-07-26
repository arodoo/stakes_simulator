"""Use case for getting coordinates."""

from typing import Optional
from ...domain.value_objects.coordinate import Coordinate
from ...domain.value_objects.view_type import ViewType
from ...infrastructure.repositories.vehicle_data_repository import VehicleDataRepository
from ...domain.entities.coordinate_modification import CoordinateModification


class GetCoordinateUseCase:
    """Use case for retrieving coordinates with modifications."""
    
    def __init__(
        self, 
        repository: VehicleDataRepository,
        modifications: dict = None
    ):
        """Initialize with repository and modifications."""
        self.repository = repository
        self.modifications = modifications or {}
    
    def get_original_coordinate(self, view: ViewType, index: int) -> Coordinate:
        """Get the original coordinate without modifications."""
        return self.repository.get_coordinate(view, index)
    
    def get_modified_coordinate(self, view: ViewType, index: int) -> Coordinate:
        """Get coordinate with modifications applied."""
        original = self.get_original_coordinate(view, index)
        
        view_modifications = self.modifications.get(view.value, {})
        if index in view_modifications:
            modification = view_modifications[index]
            return modification.modified_coordinate
        
        return original
