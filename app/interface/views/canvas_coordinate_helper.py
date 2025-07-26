"""Canvas coordinate utilities."""

from typing import Tuple


class CanvasCoordinateHelper:
    """Helper for coordinate transformations on canvas."""
    
    def __init__(self, data_service, view_name: str, width: int, height: int):
        """Initialize coordinate helper."""
        self.data_service = data_service
        self.view_name = view_name
        self.width = width
        self.height = height
        
        # Get extents for scaling
        self.min_x, self.min_y, self.max_x, self.max_y = data_service.get_extents(view_name)
        
        # Calculate scaling factors with padding
        padding = 10
        self.scale_x = (width - 2 * padding) / (self.max_x - self.min_x) if self.max_x != self.min_x else 1
        self.scale_y = (height - 2 * padding) / (self.max_y - self.min_y) if self.max_y != self.min_y else 1
        self.offset_x = padding
        self.offset_y = padding
    
    def to_canvas(self, x: float, y: float) -> Tuple[float, float]:
        """Convert data coordinates to canvas coordinates."""
        cx = (x - self.min_x) * self.scale_x + self.offset_x
        cy = self.height - ((y - self.min_y) * self.scale_y + self.offset_y)
        return cx, cy
    
    def from_canvas(self, cx: float, cy: float) -> Tuple[float, float]:
        """Convert canvas coordinates to data coordinates."""
        x = (cx - self.offset_x) / self.scale_x + self.min_x
        y = (self.height - cy - self.offset_y) / self.scale_y + self.min_y
        return x, y
