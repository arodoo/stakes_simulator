"""Use case for loading vehicle data."""

from ...infrastructure.repositories.vehicle_data_repository import VehicleDataRepository


class LoadVehicleDataUseCase:
    """Use case for loading vehicle data from database."""

    def __init__(self, repository: VehicleDataRepository):
        """Initialize with repository dependency."""
        self.repository = repository

    def execute(self) -> int:
        """Execute the use case to load all vehicle data.

        Returns:
            int: Total number of records loaded

        Raises:
            RuntimeError: If database connection fails
            ValueError: If data tables have mismatched row counts
        """
        self.repository.load_all_data()
        return self.repository.get_total_records()
