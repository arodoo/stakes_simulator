"""Use case for updating coordinates."""

from ...domain.value_objects.coordinate import Coordinate
from ...domain.value_objects.view_type import ViewType
from ...domain.entities.coordinate_modification import CoordinateModification
from ...domain.services.coordinate_transformation_service import (
    CoordinateTransformationService,
)
from ...infrastructure.repositories.vehicle_data_repository import VehicleDataRepository


class UpdateCoordinateUseCase:
    """Use case for updating coordinate modifications."""

    def __init__(self, repository: VehicleDataRepository, modifications: dict):
        """Initialize with repository and modifications store."""
        self.repository = repository
        self.modifications = modifications
        self.transformation_service = CoordinateTransformationService()

    def execute(self, view: ViewType, index: int, new_coordinate: Coordinate) -> None:
        """Update coordinate for a given view and record index."""
        original = self.repository.get_coordinate(view, index)

        # Create modification
        modification = self.transformation_service.create_modification(
            record_index=index,
            view=view,
            original_coordinate=original,
            new_coordinate=new_coordinate,
        )

        # Store or remove modification based on significance
        view_modifications = self.modifications.setdefault(view.value, {})

        if modification.is_significant():
            view_modifications[index] = modification
        else:
            # Remove any existing modification if delta is negligible
            view_modifications.pop(index, None)
