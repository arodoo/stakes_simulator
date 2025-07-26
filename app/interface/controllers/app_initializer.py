"""Application initialization logic."""

import tkinter as tk
from typing import Dict, Callable

from ...application.services.data_manager_service import DataManagerService
from .playback_controller import PlaybackController
from .export_handler import ExportHandler
from .reload_handler import ReloadHandler


class AppInitializer:
    """Handles application initialization."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the app components."""
        self.root = root
        self.root.title("Vehicle Trajectory Emulator")
        
        # Initialize services
        try:
            self.data_service = DataManagerService()
            self.data_service.initialize()
        except Exception as exc:
            print(f"ERROR: Failed to initialise data: {exc}")
            raise
    
    def create_controllers(self, update_callback: Callable[[int], None],
                          status_callback: Callable[[str], None]) -> Dict[str, object]:
        """Create and return controller instances."""
        playback_ctrl = PlaybackController(
            self.data_service.total_records,
            update_callback
        )
        
        export_handler = ExportHandler(
            self.data_service,
            status_callback
        )
        
        reload_handler = ReloadHandler(
            self.data_service,
            playback_ctrl,
            status_callback,
            update_callback
        )
        
        return {
            'playback_ctrl': playback_ctrl,
            'export_handler': export_handler,
            'reload_handler': reload_handler,
            'data_service': self.data_service
        }
