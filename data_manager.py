"""
data_manager.py
~~~~~~~~~~~~~~~~

This module defines the :class:`DataManager` class which encapsulates
all logic related to loading data from the database, normalising
coordinate data and keeping track of per‐record calibration
adjustments.  It also provides an export facility for writing
calibrated data sets back to new Excel files.

The data manager makes no assumptions about the user interface – it
merely exposes a clean API for retrieving and setting coordinate
values.  Error handling and logging are performed at load time to
ensure that the rest of the application can operate safely.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Tuple, List

import pandas as pd
from .database.connection import get_engine

class DataManager:
    """Load and provide access to vehicle trajectory data from database.

    The manager will connect to the database and load data from the 
    ``map``, ``bamboopattern``, ``centerpos2x`` and ``largescreenpixelpos`` 
    tables. Database connection issues trigger a ``RuntimeError`` at
    initialisation time.

    Attributes
    ----------
    total_records: int
        Number of rows in each of the data tables.  All tables
        must contain the same number of rows; otherwise a
        ``ValueError`` is raised.

    modifications: Dict[str, Dict[int, Tuple[float, float]]]
        Nested dictionary storing per-record coordinate adjustments for
        each view.  For instance ``modifications['bamboopattern'][123]``
        yields a tuple ``(dx, dy)`` describing how much to add to the
        original ``vehicleleft`` and ``top`` values for record 123.
    """

    def __init__(self) -> None:
        # Database engine
        self.engine = get_engine()
        # DataFrames loaded from database
        self.map_df: pd.DataFrame | None = None
        self.bamboopattern_df: pd.DataFrame | None = None
        self.centerpos2x_df: pd.DataFrame | None = None
        self.largescreenpixelpos_df: pd.DataFrame | None = None
        # Store min/max values for scaling
        self.extents: Dict[str, Tuple[float, float, float, float]] = {}
        # modifications per view
        self.modifications: Dict[str, Dict[int, Tuple[float, float]]] = {
            'bamboopattern': {},
            'centerpos2x': {},
            'largescreenpixelpos': {},
        }
        self.total_records: int = 0

        # Attempt to load data
        self._load_data()
        self._compute_extents()

    def _load_data(self) -> None:
        """Internal method to read the required data from database tables.

        Raises
        ------
        RuntimeError
            If database connection fails or tables cannot be accessed.

        ValueError
            If the database tables contain differing numbers of rows.
        """
        required_tables = {
            'map': 'map',
            'bamboopattern': 'bamboopattern',
            'centerpos2x': 'centerpos2x',
            'largescreenpixelpos': 'largescreenpixelpos',
        }
        data_frames = {}
        
        try:
            with self.engine.connect() as conn:
                for key, table_name in required_tables.items():
                    try:
                        # Load data ordered by magId to ensure consistent ordering
                        query = f"SELECT * FROM {table_name} ORDER BY magId"
                        df = pd.read_sql(query, conn)
                        if df.empty:
                            raise RuntimeError(f"Table '{table_name}' is empty")
                        data_frames[key] = df
                    except Exception as exc:
                        raise RuntimeError(f"Failed to load table '{table_name}': {exc}")
        except Exception as exc:
            raise RuntimeError(f"Database connection failed: {exc}")

        # Ensure all tables have the same number of rows
        lengths = {key: len(df) for key, df in data_frames.items()}
        if len(set(lengths.values())) != 1:
            raise ValueError(f"Input files have mismatched row counts: {lengths}")

        self.total_records = next(iter(lengths.values()))
        # Assign to attributes
        self.map_df = data_frames['map']
        self.bamboopattern_df = data_frames['bamboopattern']
        self.centerpos2x_df = data_frames['centerpos2x']
        self.largescreenpixelpos_df = data_frames['largescreenpixelpos']

    def _compute_extents(self) -> None:
        """Compute min/max extents for coordinate scaling.

        For each view we determine the range of x and y values across
        the entire dataset.  These ranges are later used to map real
        coordinates onto the canvas coordinate system.
        """
        if self.bamboopattern_df is not None:
            xs = self.bamboopattern_df['vehicleleft']
            ys = self.bamboopattern_df['top']
            self.extents['bamboopattern'] = (float(xs.min()), float(xs.max()), float(ys.min()), float(ys.max()))
        if self.centerpos2x_df is not None:
            xs = self.centerpos2x_df['xCoordinate']
            ys = self.centerpos2x_df['yCoordinate']
            self.extents['centerpos2x'] = (float(xs.min()), float(xs.max()), float(ys.min()), float(ys.max()))
        if self.largescreenpixelpos_df is not None:
            xs = self.largescreenpixelpos_df['xCoordinate']
            ys = self.largescreenpixelpos_df['yCoordinate']
            self.extents['largescreenpixelpos'] = (float(xs.min()), float(xs.max()), float(ys.min()), float(ys.max()))

    def get_original_coord(self, view: str, index: int) -> Tuple[float, float]:
        """Return the raw coordinate for a given view and record index.

        Parameters
        ----------
        view: str
            One of ``'bamboopattern'``, ``'centerpos2x'`` or
            ``'largescreenpixelpos'``.
        index: int
            Row index of the coordinate to fetch.  Must be in the
            inclusive range ``[0, total_records-1]``.

        Returns
        -------
        (float, float)
            Tuple of (x, y) for the requested record.
        """
        if not 0 <= index < self.total_records:
            raise IndexError(f"Record index {index} out of bounds")
        if view == 'bamboopattern':
            row = self.bamboopattern_df.iloc[index]
            return float(row['vehicleleft']), float(row['top'])
        elif view == 'centerpos2x':
            row = self.centerpos2x_df.iloc[index]
            return float(row['xCoordinate']), float(row['yCoordinate'])
        elif view == 'largescreenpixelpos':
            row = self.largescreenpixelpos_df.iloc[index]
            return float(row['xCoordinate']), float(row['yCoordinate'])
        else:
            raise KeyError(f"Unknown view '{view}'")

    def get_coord(self, view: str, index: int) -> Tuple[float, float]:
        """Return the coordinate for a given view and index with modifications.

        This method adds any stored per-record modifications to the
        original coordinate before returning it.
        """
        orig_x, orig_y = self.get_original_coord(view, index)
        mod = self.modifications.get(view, {})
        if index in mod:
            dx, dy = mod[index]
        else:
            dx, dy = 0.0, 0.0
        return orig_x + dx, orig_y + dy

    def set_coord(self, view: str, index: int, new_x: float, new_y: float) -> None:
        """Set a new coordinate for a given view and record index.

        The method computes a delta between the new coordinate and the
        original coordinate and stores it in the modifications
        dictionary.  A delta of (0, 0) will remove any existing
        modification for that index.
        """
        orig_x, orig_y = self.get_original_coord(view, index)
        dx = new_x - orig_x
        dy = new_y - orig_y
        # Only store non-zero adjustments to keep memory usage low
        if abs(dx) > 1e-9 or abs(dy) > 1e-9:
            self.modifications.setdefault(view, {})[index] = (dx, dy)
        else:
            # Remove any existing modification
            self.modifications.get(view, {}).pop(index, None)

    def scale_to_canvas(self, view: str, x: float, y: float, width: int, height: int) -> Tuple[float, float]:
        """Scale real coordinates to canvas space.

        Coordinates in the Excel files are often large values measured in
        pixels or metres.  Canvas coordinates on the other hand live
        in the range [0, width] x [0, height] with (0, 0) in the top
        left corner.  This method maps the supplied (x, y) onto that
        coordinate system based on the precomputed extents for the
        specified view.

        The y-axis is inverted because canvas coordinates increase
        downwards whereas conventional Cartesian coordinates increase
        upwards.
        """
        if view not in self.extents:
            raise KeyError(f"Unknown view '{view}' for scaling")
        min_x, max_x, min_y, max_y = self.extents[view]
        # Avoid division by zero if extents are degenerate
        x_range = max(max_x - min_x, 1e-9)
        y_range = max(max_y - min_y, 1e-9)
        norm_x = (x - min_x) / x_range
        norm_y = (y - min_y) / y_range
        canvas_x = norm_x * width
        # invert y axis: top of canvas is 0, bottom is height
        canvas_y = (1.0 - norm_y) * height
        return canvas_x, canvas_y

    def scale_from_canvas(self, view: str, canvas_x: float, canvas_y: float, width: int, height: int) -> Tuple[float, float]:
        """Invert the canvas scaling back to real coordinates.

        This is essentially the inverse operation of
        :meth:`scale_to_canvas`.  Given a point expressed in canvas
        coordinates it returns the corresponding real world coordinate
        according to the extents of the specified view.  The
        appropriate extents are looked up to perform this mapping.
        """
        if view not in self.extents:
            raise KeyError(f"Unknown view '{view}' for scaling")
        min_x, max_x, min_y, max_y = self.extents[view]
        x_range = max(max_x - min_x, 1e-9)
        y_range = max(max_y - min_y, 1e-9)
        norm_x = canvas_x / max(width, 1e-9)
        # invert y axis
        norm_y = 1.0 - (canvas_y / max(height, 1e-9))
        real_x = min_x + norm_x * x_range
        real_y = min_y + norm_y * y_range
        return real_x, real_y

    def export_calibrated(self, output_dir: str) -> Dict[str, str]:
        """Write calibrated datasets out to new Excel files.

        Parameters
        ----------
        output_dir: str
            Directory where the calibrated Excel files will be saved.  If
            the directory does not exist it will be created.

        Returns
        -------
        Dict[str, str]
            A mapping of view names to the filenames that were
            written.  The names will follow the pattern
            ``<view>_calibrated.xlsx``.

        Raises
        ------
        OSError
            If the output directory cannot be created.
        """
        os.makedirs(output_dir, exist_ok=True)
        written_files: Dict[str, str] = {}

        for view, df in [('bamboopattern', self.bamboopattern_df),
                         ('centerpos2x', self.centerpos2x_df),
                         ('largescreenpixelpos', self.largescreenpixelpos_df)]:
            if df is None:
                continue
            new_df = df.copy()
            mods = self.modifications.get(view, {})
            for index, (dx, dy) in mods.items():
                if view == 'bamboopattern':
                    new_df.at[index, 'vehicleleft'] = df.at[index, 'vehicleleft'] + dx
                    new_df.at[index, 'top'] = df.at[index, 'top'] + dy
                elif view == 'centerpos2x':
                    new_df.at[index, 'xCoordinate'] = df.at[index, 'xCoordinate'] + dx
                    new_df.at[index, 'yCoordinate'] = df.at[index, 'yCoordinate'] + dy
                elif view == 'largescreenpixelpos':
                    new_df.at[index, 'xCoordinate'] = df.at[index, 'xCoordinate'] + dx
                    new_df.at[index, 'yCoordinate'] = df.at[index, 'yCoordinate'] + dy
                # Do nothing for map_df, as calibration only applies to
                # visualization datasets
            filename = f"{view}_calibrated.xlsx"
            path = os.path.join(output_dir, filename)
            try:
                new_df.to_excel(path, index=False)
            except Exception as exc:
                raise RuntimeError(f"Failed to write {view} data to '{path}': {exc}")
            written_files[view] = path
        return written_files
