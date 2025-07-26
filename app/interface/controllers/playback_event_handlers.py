"""Playback event handlers."""

from typing import Callable


class PlaybackEventHandlers:
    """Handles playback-related UI events."""
    
    def __init__(self, playback_ctrl, ui_components: dict, 
                 schedule_callback: Callable[[], None]):
        """Initialize event handlers."""
        self.playback_ctrl = playback_ctrl
        self.playback_controls = ui_components['playback_controls']
        self.status_display = ui_components['status_display']
        self.schedule_callback = schedule_callback
    
    def toggle_play(self) -> None:
        """Toggle play/pause."""
        playing = self.playback_ctrl.toggle_play()
        text = "Pause" if playing else "Play"
        status = "Playing" if playing else "Paused"
        
        self.playback_controls.set_play_text(text)
        self.status_display.set_status(status)
        
        if playing:
            self.schedule_callback()
    
    def step_forward(self) -> None:
        """Step forward one frame."""
        success = self.playback_ctrl.step_forward()
        if not success:
            self.status_display.set_status("Already at end")
    
    def step_back(self) -> None:
        """Step back one frame."""
        success = self.playback_ctrl.step_back()
        if not success:
            self.status_display.set_status("Already at beginning")
    
    def reset(self) -> None:
        """Reset to start."""
        self.playback_ctrl.reset()
        self.playback_controls.set_play_text("Play")
        self.status_display.set_status("Reset to start")
    
    def on_speed_change(self, value: int) -> None:
        """Handle speed change."""
        self.playback_ctrl.set_speed(value)
