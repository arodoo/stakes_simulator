"""Reload data handler."""

from typing import Callable
from ...application.services.data_manager_service import DataManagerService
from .playback_controller import PlaybackController


class ReloadHandler:
    """Handles data reload operations."""
    
    def __init__(self, data_service: DataManagerService, 
                 playback_ctrl: PlaybackController,
                 status_callback: Callable[[str], None],
                 update_callback: Callable[[int], None]):
        """Initialize reload handler."""
        self.data_service = data_service
        self.playback_ctrl = playback_ctrl
        self.status_callback = status_callback
        self.update_callback = update_callback
    
    def reload_data(self) -> None:
        """Reload data from database and update views."""
        try:
            self.status_callback("Reloading data from database...")
            self.data_service.reload_data()
            self.playback_ctrl.update_total_records(self.data_service.total_records)
            self.update_callback(0)  # Reset to first record
            self.status_callback("Data reloaded successfully!")
        except Exception as exc:
            self.status_callback(f"Error reloading data: {exc}")
