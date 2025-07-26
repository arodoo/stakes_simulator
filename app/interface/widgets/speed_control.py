"""Speed control widget."""

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable


class SpeedControl:
    """Speed control slider widget."""
    
    def __init__(self, parent: tk.Widget, callback: Optional[Callable] = None):
        """Initialize speed control."""
        self.parent = parent
        self.callback = callback
        self.speed_var = tk.IntVar(value=1)
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Create speed control widgets."""
        speed_label = ttk.Label(self.parent, text="Speed:")
        speed_label.pack(side=tk.LEFT, padx=(20, 2))
        
        self.speed_slider = ttk.Scale(
            self.parent, from_=1, to=100, orient=tk.HORIZONTAL,
            variable=self.speed_var, command=self._on_speed_change
        )
        self.speed_slider.pack(side=tk.LEFT, padx=2)
    
    def _on_speed_change(self, event: Optional[str] = None) -> None:
        """Handle speed slider changes."""
        if self.callback:
            value = self.speed_var.get()
            self.callback(max(1, int(value)))

    def set_callback(self, callback: Callable) -> None:
        """Set the speed change callback."""
        self.callback = callback
