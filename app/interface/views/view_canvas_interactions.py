"""Continuation of ViewCanvas class with marker and interaction methods."""

    def update_marker(self, index: int) -> None:
        """Update the position of the vehicle marker."""
        self.current_index = index
        try:
            x, y = self.data_service.get_coord(self.view_name, index)
            cx, cy = self._scale_to_canvas(x, y)
            r = max(3, min(self.width, self.height) * 0.01)
            
            if self.marker_id is None:
                self.marker_id = self.create_oval(cx - r, cy - r, cx + r, cy + r,
                                                  fill='red', outline='black')
            else:
                self._move_marker_to(cx, cy)
        except Exception as exc:
            print(f"[ViewCanvas] Failed to update marker for {self.view_name}: {exc}")

    def _move_marker_to(self, cx: float, cy: float) -> None:
        """Move the existing marker to new canvas coordinates."""
        current_coords = self.coords(self.marker_id)
        x1, y1, x2, y2 = current_coords
        old_cx = (x1 + x2) / 2.0
        old_cy = (y1 + y2) / 2.0
        dx = cx - old_cx
        dy = cy - old_cy
        self.move(self.marker_id, dx, dy)    def _scale_to_canvas(self, x: float, y: float) -> tuple[float, float]:
        """Scale world coordinates to canvas coordinates."""
        min_x, min_y, max_x, max_y = self.data_service.get_extents(self.view_name)
        cx = (x - min_x) / (max_x - min_x) * self.width
        cy = (y - min_y) / (max_y - min_y) * self.height
        
        # Flip Y axis for BambooPattern so UW* is at bottom and DE* is at top
        if self.view_name == "bamboopattern":
            cy = self.height - cy
            
        return cx, cy

    def _scale_from_canvas(self, cx: float, cy: float) -> tuple[float, float]:
        """Scale canvas coordinates to world coordinates."""
        min_x, min_y, max_x, max_y = self.data_service.get_extents(self.view_name)
        
        # Flip Y axis for BambooPattern 
        if self.view_name == "bamboopattern":
            cy = self.height - cy
            
        x = min_x + (cx / self.width) * (max_x - min_x)
        y = min_y + (cy / self.height) * (max_y - min_y)
        return x, y
