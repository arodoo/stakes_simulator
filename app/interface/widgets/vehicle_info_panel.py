"""Vehicle position info widget."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any


class VehicleInfoPanel:
    """Panel showing current vehicle position data."""

    def __init__(self, parent: tk.Widget, view_name: str):
        """Initialize vehicle info panel."""
        self.view_name = view_name
        self.data = {}

        # Create frame
        self.frame = ttk.LabelFrame(parent, text=f"{view_name.capitalize()} Data")
        self.frame.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=2)

        # Create text widget for data display
        self.text_widget = tk.Text(
            self.frame, height=3, wrap=tk.WORD, font=("Consolas", 8)
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.text_widget.config(state=tk.DISABLED)

    def update_data(self, data: Dict[str, Any]) -> None:
        """Update displayed data."""
        self.data = data
        self._refresh_display()

    def _refresh_display(self) -> None:
        """Refresh the display with current data."""
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete(1.0, tk.END)

        if self.data:
            # Format data as key: value pairs
            lines = []
            for key, value in self.data.items():
                formatted_value = (
                    f"{value:.2f}" if isinstance(value, float) else str(value)
                )
                lines.append(f"{key}: {formatted_value}")

            self.text_widget.insert(1.0, " | ".join(lines))

        self.text_widget.config(state=tk.DISABLED)
