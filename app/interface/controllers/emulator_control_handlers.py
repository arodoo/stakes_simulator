"""Control panel creation and event handlers for EmulatorController."""

    def _create_control_panel(self) -> None:
        """Create the control panel with all widgets."""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        # Create control widgets
        callbacks = {
            'toggle_play': self.toggle_play,
            'step_back': self.step_back,
            'step_forward': self.step_forward,
            'reset': self.reset
        }
        
        self.playback_controls = PlaybackControls(control_frame, callbacks)
        self.speed_control = SpeedControl(control_frame, self._on_speed_change)
        self.export_button = ExportButton(control_frame, self.export_data)
        self.status_display = StatusDisplay(control_frame)

    def _on_speed_change(self, value: int) -> None:
        """Handle speed change from speed control."""
        self.speed_step = value
        if self.playing:
            self.status_display.set_status(f"Speed set to {self.speed_step}")

    def toggle_play(self) -> None:
        """Toggle between play and pause states."""
        self.playing = not self.playing
        if self.playing:
            self.playback_controls.set_play_text("Pause")
            self.status_display.set_status("Playing")
            self._schedule_next_tick()
        else:
            self.playback_controls.set_play_text("Play")
            self.status_display.set_status("Paused")

    def _schedule_next_tick(self) -> None:
        """Schedule the next playback update when playing."""
        if self.playing:
            self.root.after(100, self._tick)

    def _tick(self) -> None:
        """Advance the playback and update the UI."""
        if not self.playing:
            return
        
        self.current_index += self.speed_step
        if self.current_index >= self.data_service.total_records:
            self.current_index = self.data_service.total_records - 1
            self.playing = False
            self.playback_controls.set_play_text("Play")
            self.status_display.set_status("Reached end of data")
        
        self._update_all_views()
        self._schedule_next_tick()
