"""Data manager service for the application layer."""

from typing import Dict, Tuple
from ...domain.value_objects.view_type import ViewType
from ...infrastructure.repositories.vehicle_data_repository import VehicleDataRepository
from ...infrastructure.export.excel_export_service import ExcelExportService


class DataManagerService:
    """Application service for managing vehicle data operations."""

    def __init__(self):
        """Initialize the data manager service."""
        self.repository = VehicleDataRepository()
        self.export_service = ExcelExportService()
        self.total_records: int = 0

    def initialize(self) -> None:
        """Initialize data from repository."""
        self.repository.load_all_data()
        self.total_records = self.repository.get_total_records()

    def get_coord(self, view_name: str, index: int) -> Tuple[float, float]:
        """Get coordinate for a view and index."""
        view_type = ViewType.from_string(view_name)
        coord = self.repository.get_coordinate(view_type, index)
        return coord.x, coord.y

    def get_original_coord(self, view_name: str, index: int) -> Tuple[float, float]:
        """Get original coordinate (same as get_coord for now)."""
        return self.get_coord(view_name, index)

    def set_coord(self, view_name: str, index: int, x: float, y: float) -> None:
        """Set coordinate for a view and index."""
        view_type = ViewType.from_string(view_name)
        self.repository.update_coordinate(view_type, index, x, y)

    def get_extents(self, view_name: str) -> Tuple[float, float, float, float]:
        """Get extents for a view."""
        view_type = ViewType.from_string(view_name)
        extents = self.repository.get_extents(view_type)
        return extents.min_x, extents.min_y, extents.max_x, extents.max_y

    def export_calibrated(self, output_dir: str) -> Dict[str, str]:
        """Export calibrated data to Excel files."""
        written_files = {}
        for view_type in ViewType:
            records = self.repository.get_all_records(view_type)
            file_path = self.export_service.export_data(
                records, view_type.value, output_dir
            )
            written_files[view_type.value] = file_path
        return written_files

    def reload_data(self) -> None:
        """Reload all data from database."""
        self.repository.load_all_data()
        self.total_records = self.repository.get_total_records()
