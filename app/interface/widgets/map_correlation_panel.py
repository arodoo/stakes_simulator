"""Map correlation panel widget."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any


class MapCorrelationPanel:
    """Panel showing correlation between maps and master table."""
    
    def __init__(self, parent: tk.Widget):
        """Initialize map correlation panel."""
        self.data = {}
        
        # Create main frame
        self.frame = ttk.LabelFrame(parent, text="Map Correlation & Master Data")
        self.frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create frames for each section
        self.master_frame = ttk.Frame(self.notebook)
        self.correlation_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.master_frame, text="Master Data (map)")
        self.notebook.add(self.correlation_frame, text="Correlation")
        
        # Create text widgets
        self.master_text = tk.Text(self.master_frame, height=3, wrap=tk.WORD, font=("Consolas", 8))
        self.master_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.master_text.config(state=tk.DISABLED)
        
        self.correlation_text = tk.Text(self.correlation_frame, height=3, wrap=tk.WORD, font=("Consolas", 8))
        self.correlation_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        self.correlation_text.config(state=tk.DISABLED)
    
    def update_data(self, master_data: Dict[str, Any], correlation_data: Dict[str, Dict[str, Any]]) -> None:
        """Update displayed data."""
        self.data = {"master": master_data, "correlation": correlation_data}
        self._refresh_display()
    
    def _refresh_display(self) -> None:
        """Refresh the display with current data."""
        self._update_master_tab()
        self._update_correlation_tab()
    
    def _update_master_tab(self) -> None:
        """Update master data tab."""
        self.master_text.config(state=tk.NORMAL)
        self.master_text.delete(1.0, tk.END)
        
        master = self.data.get("master", {})
        if master:
            # Show key master table fields
            key_fields = ["magId", "stake", "segment", "coordinateX", "coordinateY", "cruisingSpeed"]
            lines = []
            for field in key_fields:
                if field in master:
                    value = master[field]
                    formatted = f"{value:.2f}" if isinstance(value, float) else str(value)
                    lines.append(f"{field}: {formatted}")
            self.master_text.insert(1.0, " | ".join(lines))
        
        self.master_text.config(state=tk.DISABLED)
    
    def _update_correlation_tab(self) -> None:
        """Update correlation tab."""
        self.correlation_text.config(state=tk.NORMAL)
        self.correlation_text.delete(1.0, tk.END)
        
        correlation = self.data.get("correlation", {})
        if correlation:
            lines = []
            for view_name, view_data in correlation.items():
                coord_info = f"{view_name}: "
                if view_name == "bamboopattern":
                    coord_info += f"left={view_data.get('vehicleleft', 'N/A')}, top={view_data.get('top', 'N/A')}"
                else:
                    coord_info += f"X={view_data.get('xCoordinate', 'N/A')}, Y={view_data.get('yCoordinate', 'N/A')}"
                lines.append(coord_info)
            self.correlation_text.insert(1.0, " | ".join(lines))
        
        self.correlation_text.config(state=tk.DISABLED)