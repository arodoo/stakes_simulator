"""Reload button widget."""

import tkinter as tk
from tkinter import ttk
from typing import Callable, Optional


class ReloadButton:
    """Button for reloading data from database."""

    def __init__(self, parent: tk.Widget, callback: Optional[Callable] = None):
        """Initialize reload button."""
        self.callback = callback
        self.button = ttk.Button(parent, text="🔄 Reload Data", command=self._on_click)
        self.button.pack(side=tk.LEFT, padx=(5, 0))

    def _on_click(self) -> None:
        """Handle button click."""
        if self.callback:
            self.callback()

    def set_callback(self, callback: Callable) -> None:
        """Set the callback function."""
        self.callback = callback
