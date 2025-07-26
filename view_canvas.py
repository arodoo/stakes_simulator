"""
view_canvas.py
~~~~~~~~~~~~~~

Defines the :class:`ViewCanvas` which encapsulates a Tkinter
``Canvas`` widget tailored for drawing the trajectory of a single
vehicle view.  It draws the entire path once at initialisation and
updates a marker representing the vehicle's current position on each
call to :meth:`update_marker`.  The widget also handles mouse
interaction to allow users to drag the marker and thereby calibrate
individual points.

Usage
-----

``ViewCanvas`` instances should be created by passing in a
:class:`vehicle_emulator.data_manager.DataManager` object, the name of
the view they represent (``'bamboopattern'``, ``'centerpos2x'`` or
``'largescreenpixelpos'``) and the desired width and height.  They can
then be packed or gridded into a containing frame.  The marker is
drawn as a small circle, the size of which scales with the canvas
dimensions.

Example::

    dm = DataManager('/path/to/data')
    canvas = ViewCanvas(root, dm, 'bamboopattern', width=400, height=300)
    canvas.grid(row=0, column=0)
    canvas.update_marker(0)

The ``update_marker`` method should be called whenever the current
record index changes.  Dragging the marker automatically updates
modifications inside the data manager.
"""

from __future__ import annotations

import tkinter as tk
from typing import Optional, Tuple

from .data_manager import DataManager


class ViewCanvas(tk.Canvas):
    """A canvas which draws a precomputed path and a movable vehicle marker."""

    def __init__(self, master: tk.Misc, data_manager: DataManager, view_name: str,
                 width: int = 400, height: int = 300, **kwargs) -> None:
        super().__init__(master, width=width, height=height,
                         background='white', highlightthickness=1,
                         highlightbackground='black', **kwargs)
        self.data_manager = data_manager
        self.view_name = view_name
        self.width = width
        self.height = height
        self.current_index: int = 0
        # Canvas ids for marker and optional dragging highlight
        self.marker_id: Optional[int] = None
        self.dragging: bool = False
        # Precompute and draw the full path
        self._draw_path()
        # Bind mouse events for dragging
        self.bind('<ButtonPress-1>', self._on_press)
        self.bind('<B1-Motion>', self._on_drag)
        self.bind('<ButtonRelease-1>', self._on_release)

    def _draw_path(self) -> None:
        """Draw the full polyline path for this view."""
        try:
            coords: list[float] = []
            # Iterate over all records once and collect scaled positions
            for idx in range(self.data_manager.total_records):
                x, y = self.data_manager.get_original_coord(self.view_name, idx)
                cx, cy = self.data_manager.scale_to_canvas(
                    self.view_name, x, y, self.width, self.height)
                coords.extend([cx, cy])
            # Draw the path with a light grey line
            self.create_line(*coords, fill='#cccccc', width=1)
        except Exception as exc:
            # If any error occurs while drawing the path, write to console
            print(f"[ViewCanvas] Failed to draw path for {self.view_name}: {exc}")

    def update_marker(self, index: int) -> None:
        """Update the position of the vehicle marker.

        Parameters
        ----------
        index: int
            Record index for which to display the marker.
        """
        self.current_index = index
        try:
            x, y = self.data_manager.get_coord(self.view_name, index)
            cx, cy = self.data_manager.scale_to_canvas(
                self.view_name, x, y, self.width, self.height)
            r = max(3, min(self.width, self.height) * 0.01)  # marker radius
            if self.marker_id is None:
                # First time: create the marker
                self.marker_id = self.create_oval(cx - r, cy - r, cx + r, cy + r,
                                                  fill='red', outline='black')
            else:
                # Move the existing marker
                current_coords = self.coords(self.marker_id)
                # Compute delta from current coords to new coords
                # Coords returns bounding box (x1, y1, x2, y2)
                x1, y1, x2, y2 = current_coords
                old_cx = (x1 + x2) / 2.0
                old_cy = (y1 + y2) / 2.0
                dx = cx - old_cx
                dy = cy - old_cy
                self.move(self.marker_id, dx, dy)
        except Exception as exc:
            print(f"[ViewCanvas] Failed to update marker for {self.view_name}: {exc}")

    def _on_press(self, event: tk.Event) -> None:
        """Start dragging the marker if click is near it."""
        if self.marker_id is None:
            return
        # Check if click is within marker's bounding box
        x1, y1, x2, y2 = self.bbox(self.marker_id)
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            self.dragging = True
        else:
            self.dragging = False

    def _on_drag(self, event: tk.Event) -> None:
        """Handle dragging of the marker to calibrate coordinates."""
        if not self.dragging or self.marker_id is None:
            return
        # Constrain dragging within canvas bounds
        canvas_x = max(0, min(event.x, self.width))
        canvas_y = max(0, min(event.y, self.height))
        # Move marker visually
        x1, y1, x2, y2 = self.bbox(self.marker_id)
        old_cx = (x1 + x2) / 2.0
        old_cy = (y1 + y2) / 2.0
        dx = canvas_x - old_cx
        dy = canvas_y - old_cy
        self.move(self.marker_id, dx, dy)
        # Convert to real coordinates and set modification
        try:
            real_x, real_y = self.data_manager.scale_from_canvas(
                self.view_name, canvas_x, canvas_y, self.width, self.height)
            self.data_manager.set_coord(self.view_name, self.current_index, real_x, real_y)
        except Exception as exc:
            print(f"[ViewCanvas] Failed to set calibrated coordinate for {self.view_name}: {exc}")

    def _on_release(self, event: tk.Event) -> None:
        """Stop dragging."""
        self.dragging = False
