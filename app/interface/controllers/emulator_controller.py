"""Main application controller."""

import tkinter as tk

from .app_initializer import AppInitializer
from .ui_builder import UIBuilder
from .playback_event_handlers import PlaybackEventHandlers


class EmulatorController:
    """Main application controller coordinating all components."""

    def __init__(self, root: tk.Tk) -> None:
        """Initialize the emulator controller."""
        # Initialize app components
        self.initializer = AppInitializer(root)
        controllers = self.initializer.create_controllers(
            self._update_all_views,
            self._set_status
        )
        
        self.playback_ctrl = controllers['playback_ctrl']
        self.export_handler = controllers['export_handler']
        
        # Build UI and set up event handlers
        self._build_ui()
        self._update_all_views(0)

    def _build_ui(self) -> None:
        """Build the user interface."""
        callbacks = {
            'export': self.export_handler.export_data
        }
        
        ui_builder = UIBuilder(
            self.initializer.root, 
            self.initializer.data_service, 
            callbacks
        )
        components = ui_builder.build_interface()
        
        self.canvases = components['canvases']
        
        # Set up playback event handlers
        self.event_handlers = PlaybackEventHandlers(
            self.playback_ctrl, 
            components, 
            self._schedule_next_tick
        )
        
        # Wire up the playback controls
        self._wire_playback_controls(components)

    def _wire_playback_controls(self, components: dict) -> None:
        """Wire up playback control callbacks."""
        controls = components['playback_controls']
        controls.set_callbacks({
            'toggle_play': self.event_handlers.toggle_play,
            'step_back': self.event_handlers.step_back,
            'step_forward': self.event_handlers.step_forward,
            'reset': self.event_handlers.reset
        })
        
        speed_control = components['speed_control']
        speed_control.set_callback(self.event_handlers.on_speed_change)

    def _schedule_next_tick(self) -> None:
        """Schedule next playback update."""
        self.initializer.root.after(100, self._tick)

    def _tick(self) -> None:
        """Handle playback tick."""
        still_playing = self.playback_ctrl.tick()
        if not still_playing:
            # Use event handlers to maintain consistency
            self.event_handlers.playback_controls.set_play_text("Play")
            self.event_handlers.status_display.set_status("Reached end of data")
        else:
            self._schedule_next_tick()

    def _update_all_views(self, index: int) -> None:
        """Update all canvas views."""
        for canvas in self.canvases.values():
            canvas.update_marker(index)

    def _set_status(self, message: str) -> None:
        """Set status message."""
        self.event_handlers.status_display.set_status(message)
