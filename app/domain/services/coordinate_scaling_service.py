"""Coordinate scaling domain service."""

from typing import Tuple
from ..value_objects.coordinate import Coordinate
from ..value_objects.extents import Extents
from ..value_objects.view_type import ViewType


class CoordinateScalingService:
    """Domain service for scaling coordinates between real and canvas space."""

    @staticmethod
    def scale_to_canvas(
        coordinate: Coordinate, 
        extents: Extents, 
        canvas_width: int, 
        canvas_height: int,
        view_type: ViewType = None
    ) -> Coordinate:
        """Scale real coordinates to canvas space."""
        norm_x = (coordinate.x - extents.min_x) / extents.x_range
        norm_y = (coordinate.y - extents.min_y) / extents.y_range        canvas_x = norm_x * canvas_width
        
        # No invertimos Y ya que los datos están en orden correcto
        canvas_y = norm_y * canvas_height

        return Coordinate(canvas_x, canvas_y)

    @staticmethod
    def scale_from_canvas(
        canvas_coordinate: Coordinate,
        extents: Extents,
        canvas_width: int,
        canvas_height: int,
        view_type: ViewType = None
    ) -> Coordinate:
        """Scale canvas coordinates back to real space."""        norm_x = canvas_coordinate.x / max(canvas_width, 1e-9)
        
        # No invertimos Y ya que los datos están en orden correcto
        norm_y = canvas_coordinate.y / max(canvas_height, 1e-9)

        real_x = extents.min_x + norm_x * extents.x_range
        real_y = extents.min_y + norm_y * extents.y_range

        return Coordinate(real_x, real_y)
