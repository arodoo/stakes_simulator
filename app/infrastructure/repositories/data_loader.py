"""Data loading utilities for repository."""

import pandas as pd
from typing import Dict
from database.connection import get_engine
from ...domain.value_objects.view_type import ViewType


class DataLoader:
    """Handles data loading from database."""

    def __init__(self):
        """Initialize data loader."""
        self.engine = get_engine()

    def load_all_tables(self) -> Dict[str, pd.DataFrame]:
        """Load all required tables from database."""
        required_tables = {
            "map": "map",
            "bamboopattern": ViewType.BAMBOO_PATTERN.value,
            "centerpos2x": ViewType.CENTER_POS_2X.value,
            "largescreenpixelpos": ViewType.LARGE_SCREEN_PIXEL_POS.value,
        }

        data_frames = {}
        try:
            with self.engine.connect() as conn:
                for table_name, key in required_tables.items():
                    query = f"SELECT * FROM {table_name} ORDER BY magId"
                    df = pd.read_sql(query, conn)
                    if df.empty:
                        raise RuntimeError(f"Table '{table_name}' is empty")
                    data_frames[key] = df
        except Exception as exc:
            raise RuntimeError(f"Database connection failed: {exc}")

        return data_frames

    def validate_data_consistency(self, data_frames: Dict[str, pd.DataFrame]) -> None:
        """Validate that all tables have the same number of rows."""
        lengths = {key: len(df) for key, df in data_frames.items()}
        if len(set(lengths.values())) != 1:
            raise ValueError(f"Input files have mismatched row counts: {lengths}")
