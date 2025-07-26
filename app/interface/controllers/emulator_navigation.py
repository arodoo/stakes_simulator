"""Navigation and export methods for EmulatorController."""

    def step_forward(self) -> None:
        """Step the current index forward by one and update views."""
        if self.current_index < self.data_service.total_records - 1:
            self.current_index += 1
            self._update_all_views()
            self.status_display.set_status(f"Index: {self.current_index}")
        else:
            self.status_display.set_status("Already at end")

    def step_back(self) -> None:
        """Step the current index backward by one and update views."""
        if self.current_index > 0:
            self.current_index -= 1
            self._update_all_views()
            self.status_display.set_status(f"Index: {self.current_index}")
        else:
            self.status_display.set_status("Already at beginning")

    def reset(self) -> None:
        """Reset playback to the start."""
        self.current_index = 0
        self.playing = False
        self.playback_controls.set_play_text("Play")
        self._update_all_views()
        self.status_display.set_status("Reset to start")

    def _update_all_views(self) -> None:
        """Refresh marker positions on all canvases."""
        for canvas in self.canvases.values():
            canvas.update_marker(self.current_index)

    def export_data(self) -> None:
        """Prompt user for output directory and export calibrated data."""
        output_dir = filedialog.askdirectory(
            title="Select output directory for calibrated files"
        )
        if not output_dir:
            return
        
        try:
            written = self.data_service.export_calibrated(output_dir)
            self._show_export_results(written)
        except Exception as exc:
            print(f"ERROR: Failed to export calibrated data: {exc}")

    def _show_export_results(self, written: dict) -> None:
        """Show export results."""
        msg_lines = ["Calibrated files written:"]
        for view, path in written.items():
            msg_lines.append(f"  {view}: {os.path.basename(path)}")
        print("\n".join(msg_lines))
