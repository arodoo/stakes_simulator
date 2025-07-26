"""Status and export widgets."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable


class StatusDisplay:
    """Status display widget."""
    
    def __init__(self, parent: tk.Widget):
        """Initialize status display."""
        self.parent = parent
        self.status_var = tk.StringVar(value="Ready")
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create status display widget."""
        self.status_label = ttk.Label(self.parent, textvariable=self.status_var)
        self.status_label.pack(side=tk.RIGHT, padx=(2, 10))
    
    def set_status(self, status: str) -> None:
        """Set the status text."""
        self.status_var.set(status)


class ExportButton:
    """Export button widget."""
    
    def __init__(self, parent: tk.Widget, callback: Optional[Callable] = None):
        """Initialize export button."""
        self.parent = parent
        self.callback = callback
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create export button widget."""
        self.export_button = ttk.Button(
            self.parent, text="Export Calibrated",
            command=self.callback
        )
        self.export_button.pack(side=tk.RIGHT, padx=2)
