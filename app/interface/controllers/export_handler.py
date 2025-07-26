"""Export functionality handler."""

import os
from tkinter import filedialog
from typing import Dict, Callable


class ExportHandler:
    """Handles data export operations."""
    
    def __init__(self, data_service, status_callback: Callable[[str], None]):
        """Initialize export handler."""
        self.data_service = data_service
        self.status_callback = status_callback
    
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
            self.status_callback("Export completed successfully")
        except Exception as exc:
            error_msg = f"ERROR: Failed to export calibrated data: {exc}"
            print(error_msg)
            self.status_callback("Export failed")
    
    def _show_export_results(self, written: Dict[str, str]) -> None:
        """Show export results."""
        msg_lines = ["Calibrated files written:"]
        for view, path in written.items():
            msg_lines.append(f"  {view}: {os.path.basename(path)}")
        print("\n".join(msg_lines))
