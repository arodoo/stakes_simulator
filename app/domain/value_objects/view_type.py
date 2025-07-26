"""View type enumeration."""

from enum import Enum
from typing import List


class ViewType(Enum):
    """Enumeration of supported view types."""

    BAMBOO_PATTERN = "bamboopattern"
    CENTER_POS_2X = "centerpos2x"
    LARGE_SCREEN_PIXEL_POS = "largescreenpixelpos"

    @classmethod
    def get_all_views(cls) -> List[str]:
        """Get list of all view type values."""
        return [view.value for view in cls]

    @classmethod
    def is_valid_view(cls, view: str) -> bool:
        """Check if view string is valid."""
        return view in cls.get_all_views()

    @classmethod
    def from_string(cls, view_name: str) -> "ViewType":
        """Create ViewType from string name."""
        for view_type in cls:
            if view_type.value == view_name:
                return view_type
        raise ValueError(f"Unknown view type: {view_name}")

    def get_x_column(self) -> str:
        """Get the x coordinate column name for this view type."""
        if self == ViewType.BAMBOO_PATTERN:
            return "vehicleleft"
        return "xCoordinate"

    def get_y_column(self) -> str:
        """Get the y coordinate column name for this view type."""
        if self == ViewType.BAMBOO_PATTERN:
            return "top"
        return "yCoordinate"
