"""Mouse interaction handlers for ViewCanvas."""

    def _on_press(self, event) -> None:
        """Start dragging the marker if click is near it."""
        if self.marker_id is None:
            return
        x1, y1, x2, y2 = self.bbox(self.marker_id)
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            self.dragging = True
        else:
            self.dragging = False

    def _on_drag(self, event) -> None:
        """Handle dragging of the marker to calibrate coordinates."""
        if not self.dragging or self.marker_id is None:
            return
        
        canvas_x = max(0, min(event.x, self.width))
        canvas_y = max(0, min(event.y, self.height))
        
        self._move_marker_visually(canvas_x, canvas_y)
        self._update_coordinate(canvas_x, canvas_y)

    def _move_marker_visually(self, canvas_x: float, canvas_y: float) -> None:
        """Move marker visually on canvas."""
        x1, y1, x2, y2 = self.bbox(self.marker_id)
        old_cx = (x1 + x2) / 2.0
        old_cy = (y1 + y2) / 2.0
        dx = canvas_x - old_cx
        dy = canvas_y - old_cy
        self.move(self.marker_id, dx, dy)

    def _update_coordinate(self, canvas_x: float, canvas_y: float) -> None:
        """Update the coordinate in the data service."""
        try:
            real_x, real_y = self._scale_from_canvas(canvas_x, canvas_y)
            self.data_service.set_coord(self.view_name, self.current_index, real_x, real_y)
        except Exception as exc:
            print(f"[ViewCanvas] Failed to set calibrated coordinate for {self.view_name}: {exc}")

    def _on_release(self, event) -> None:
        """Stop dragging."""
        self.dragging = False
