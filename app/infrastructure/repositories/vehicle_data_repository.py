"""Vehicle data repository implementation."""

from typing import Dict
import pandas as pd
from ...domain.entities.vehicle_record import VehicleRecord
from ...domain.value_objects.coordinate import Coordinate
from ...domain.value_objects.view_type import ViewType
from ...domain.value_objects.extents import Extents
from .data_loader import DataLoader
from .extents_calculator import ExtentsCalculator


class VehicleDataRepository:
    """Repository for vehicle data access."""

    def __init__(self):
        """Initialize repository."""
        self.loader = DataLoader()
        self.extents_calc = ExtentsCalculator()
        self._data_frames: Dict[str, pd.DataFrame] = {}
        self._extents: Dict[str, Extents] = {}

    def load_all_data(self) -> None:
        """Load all data from database tables."""
        self._data_frames = self.loader.load_all_tables()
        self.loader.validate_data_consistency(self._data_frames)
        self._extents = self.extents_calc.compute_all_extents(self._data_frames)

    def get_total_records(self) -> int:
        """Get total number of records."""
        if "map" in self._data_frames:
            return len(self._data_frames["map"])
        return 0

    def get_coordinate(self, view_type: ViewType, index: int) -> Coordinate:
        """Get coordinate for specific view and index."""
        df = self._data_frames.get(view_type.value)
        if df is None or index >= len(df):
            raise IndexError(f"Invalid index {index} for view {view_type.value}")

        row = df.iloc[index]
        x_col = view_type.get_x_column()
        y_col = view_type.get_y_column()
        return Coordinate(float(row[x_col]), float(row[y_col]))

    def get_extents(self, view_type: ViewType) -> Extents:
        """Get coordinate extents for a view."""
        return self._extents.get(view_type.value, Extents(0, 0, 1, 1))

    def update_coordinate(
        self, view_type: ViewType, index: int, x: float, y: float
    ) -> None:
        """Update coordinate for specific view and index."""
        df = self._data_frames.get(view_type.value)
        if df is None or index >= len(df):
            raise IndexError(f"Invalid index {index} for view {view_type.value}")

        x_col = view_type.get_x_column()
        y_col = view_type.get_y_column()
        df.loc[index, x_col] = x
        df.loc[index, y_col] = y

    def get_all_records(self, view_type: ViewType) -> list[VehicleRecord]:
        """Get all records for a view type."""
        df = self._data_frames.get(view_type.value)
        if df is None:
            return []

        records = []
        x_col = view_type.get_x_column()
        y_col = view_type.get_y_column()

        for _, row in df.iterrows():
            coord = Coordinate(float(row[x_col]), float(row[y_col]))
            record = VehicleRecord(int(row["magId"]), coord)
            records.append(record)

        return records
