"""Canvas drag interaction handler."""

import tkinter as tk
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    pass


class DragHandler:
    """Handles mouse drag interactions on canvas."""

    def __init__(self, canvas: tk.Canvas, data_service, coordinate_helper):
        """Initialize drag handler."""
        self.canvas = canvas
        self.data_service = data_service
        self.coord_helper = coordinate_helper
        self.dragging: bool = False
        self.current_index: int = 0

        self._bind_events()

    def _bind_events(self) -> None:
        """Bind mouse events for dragging."""
        self.canvas.bind("<ButtonPress-1>", self._on_press)
        self.canvas.bind("<B1-Motion>", self._on_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event: tk.Event) -> None:
        """Handle mouse press event."""
        self.dragging = True

    def _on_drag(self, event: tk.Event) -> None:
        """Handle mouse drag event."""
        if not self.dragging:
            return

        # Convert canvas coordinates to data coordinates
        x, y = self.coord_helper.from_canvas(event.x, event.y)

        # Update the coordinate in the data service
        self.data_service.set_coord(
            self.coord_helper.view_name, self.current_index, x, y
        )

    def _on_release(self, event: tk.Event) -> None:
        """Handle mouse release event."""
        self.dragging = False

    def set_current_index(self, index: int) -> None:
        """Set the current index for dragging operations."""
        self.current_index = index
