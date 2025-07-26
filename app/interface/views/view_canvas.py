"""Canvas view for displaying vehicle trajectories."""

import tkinter as tk
from typing import Optional

from ...application.services.data_manager_service import DataManagerService
from .canvas_coordinate_helper import CanvasCoordinateHelper
from .path_renderer import PathRenderer
from .drag_handler import DragHandler


class ViewCanvas(tk.Canvas):
    """A canvas which draws a precomputed path and a movable vehicle marker."""

    def __init__(
        self,
        master: tk.Misc,
        data_service: DataManagerService,
        view_name: str,
        width: int = 400,
        height: int = 300,
        **kwargs,
    ) -> None:
        """Initialize the view canvas."""
        super().__init__(
            master,
            width=width,
            height=height,
            background="white",
            highlightthickness=1,
            highlightbackground="black",
            **kwargs,
        )

        self.data_service = data_service
        self.view_name = view_name
        self.current_index: int = 0
        self.marker_id: Optional[int] = None

        # Initialize helpers
        self.coord_helper = CanvasCoordinateHelper(
            data_service, view_name, width, height
        )
        self.path_renderer = PathRenderer(self, data_service, self.coord_helper)
        self.drag_handler = DragHandler(self, data_service, self.coord_helper)

        # Draw initial path
        self.path_renderer.draw_path(view_name)

    def update_marker(self, index: int) -> None:
        """Update the position of the vehicle marker."""
        if self.marker_id is not None:
            self.delete(self.marker_id)

        self.current_index = index
        self.drag_handler.set_current_index(index)

        try:
            x, y = self.data_service.get_coord(self.view_name, index)
            self.marker_id = self.path_renderer.draw_marker(x, y)
        except Exception as exc:
            print(f"[ViewCanvas] Failed to update marker: {exc}")
            self.marker_id = None
