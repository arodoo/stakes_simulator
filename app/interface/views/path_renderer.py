"""Canvas path renderer."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import tkinter as tk


class PathRenderer:
    """Renders trajectory paths on canvas."""

    def __init__(self, canvas: "tk.Canvas", data_service, coordinate_helper):
        """Initialize path renderer."""
        self.canvas = canvas
        self.data_service = data_service
        self.coord_helper = coordinate_helper

    def draw_path(self, view_name: str) -> None:
        """Draw the full polyline path for this view."""
        try:
            coords: list[float] = []
            for idx in range(self.data_service.total_records):
                x, y = self.data_service.get_original_coord(view_name, idx)
                cx, cy = self.coord_helper.to_canvas(x, y)
                coords.extend([cx, cy])

            if coords:
                self.canvas.create_line(*coords, fill="#cccccc", width=1)
        except Exception as exc:
            print(f"[PathRenderer] Failed to draw path for {view_name}: {exc}")

    def draw_marker(self, x: float, y: float, color: str = "red", size: int = 5) -> int:
        """Draw a marker at the specified coordinates."""
        cx, cy = self.coord_helper.to_canvas(x, y)
        return self.canvas.create_oval(
            cx - size,
            cy - size,
            cx + size,
            cy + size,
            fill=color,
            outline="black",
            width=1,
        )
