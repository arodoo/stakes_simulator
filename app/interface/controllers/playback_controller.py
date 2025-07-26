"""Playback control logic."""

from typing import Callable


class PlaybackController:
    """Handles playback state and operations."""
    
    def __init__(self, total_records: int, update_callback: Callable[[int], None]):
        """Initialize playback controller."""
        self.total_records = total_records
        self.update_callback = update_callback
        self.current_index: int = 0
        self.playing: bool = False
        self.speed_step: int = 1
    
    def toggle_play(self) -> bool:
        """Toggle play/pause state. Returns new playing state."""
        self.playing = not self.playing
        return self.playing
    
    def step_forward(self) -> bool:
        """Step forward one index. Returns True if successful."""
        if self.current_index < self.total_records - 1:
            self.current_index += 1
            self.update_callback(self.current_index)
            return True
        return False
    
    def step_back(self) -> bool:
        """Step back one index. Returns True if successful."""
        if self.current_index > 0:
            self.current_index -= 1
            self.update_callback(self.current_index)
            return True
        return False
    
    def reset(self) -> None:
        """Reset to start."""
        self.current_index = 0
        self.playing = False
        self.update_callback(self.current_index)
    
    def tick(self) -> bool:
        """Advance playback. Returns True if still playing."""
        if not self.playing:
            return False
            
        self.current_index += self.speed_step
        if self.current_index >= self.total_records:
            self.current_index = self.total_records - 1
            self.playing = False
            self.update_callback(self.current_index)
            return False
        
        self.update_callback(self.current_index)
        return True
    
    def set_speed(self, speed: int) -> None:
        """Set playback speed."""
        self.speed_step = speed

    def update_total_records(self, total_records: int) -> None:
        """Update total records count after data reload."""
        self.total_records = total_records
        if self.current_index >= total_records:
            self.current_index = 0
            self.update_callback(self.current_index)
