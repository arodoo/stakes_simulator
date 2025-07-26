"""Use case for exporting calibrated data."""

from typing import Dict
from ...domain.value_objects.view_type import ViewType
from ...infrastructure.repositories.vehicle_data_repository import VehicleDataRepository
from ...infrastructure.export.excel_export_service import ExcelExportService


class ExportCalibratedDataUseCase:
    """Use case for exporting calibrated vehicle data."""

    def __init__(self, repository: VehicleDataRepository, modifications: dict):
        """Initialize with repository and modifications."""
        self.repository = repository
        self.modifications = modifications
        self.export_service = ExcelExportService()

    def execute(self, output_dir: str) -> Dict[str, str]:
        """Export calibrated data to Excel files.

        Args:
            output_dir: Directory where calibrated files will be saved

        Returns:
            Dict mapping view names to written file paths

        Raises:
            OSError: If output directory cannot be created
            RuntimeError: If file writing fails
        """
        # Gather all dataframes
        data_frames = {}
        for view_type in ViewType:
            try:
                df = self.repository.get_dataframe(view_type)
                data_frames[view_type.value] = df
            except KeyError:
                # Skip views that don't exist in repository
                continue

        return self.export_service.export_calibrated_data(
            data_frames=data_frames,
            modifications=self.modifications,
            output_dir=output_dir,
        )
