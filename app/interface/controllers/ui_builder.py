"""UI builder for the main application."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Callable

from ..views.view_canvas import ViewCanvas
from ..widgets.playback_controls import PlaybackControls
from ..widgets.speed_control import SpeedControl
from ..widgets.status_and_export import StatusDisplay, ExportButton
from ..widgets.reload_button import ReloadButton


class UIBuilder:
    """Builds the user interface components."""

    def __init__(self, root: tk.Tk, data_service, callbacks: Dict[str, Callable]):
        """Initialize UI builder."""
        self.root = root
        self.data_service = data_service
        self.callbacks = callbacks
        self.canvases: Dict[str, ViewCanvas] = {}

    def build_interface(self) -> Dict[str, object]:
        """Build the complete interface and return components."""
        self._create_view_frame()
        control_widgets = self._create_control_panel()

        return {"canvases": self.canvases, **control_widgets}

    def _create_view_frame(self) -> None:
        """Create the main view frame with canvases."""
        view_frame = ttk.Frame(self.root)
        view_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)

        view_names = ["bamboopattern", "centerpos2x", "largescreenpixelpos"]
        for i, view_name in enumerate(view_names):
            self._create_view_canvas(view_frame, view_name, i)

    def _create_view_canvas(
        self, parent: ttk.Frame, view_name: str, column: int
    ) -> None:
        """Create a single view canvas."""
        frame = ttk.Frame(parent, relief=tk.SUNKEN, borderwidth=1)
        frame.grid(row=0, column=column, padx=5, pady=5, sticky="nsew")
        parent.columnconfigure(column, weight=1)

        label = ttk.Label(frame, text=view_name.capitalize())
        label.pack(side=tk.TOP, pady=(2, 2))

        canvas = ViewCanvas(frame, self.data_service, view_name, width=400, height=300)
        canvas.pack(fill=tk.BOTH, expand=True)
        self.canvases[view_name] = canvas

    def _create_control_panel(self) -> Dict[str, object]:
        """Create the control panel with all widgets."""
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        # Create empty callbacks for playback controls initially
        playback_callbacks = {}
        playback_controls = PlaybackControls(control_frame, playback_callbacks)
        speed_control = SpeedControl(control_frame, None)
        export_button = ExportButton(control_frame, self.callbacks.get("export"))
        reload_button = ReloadButton(control_frame, self.callbacks.get("reload"))
        status_display = StatusDisplay(control_frame)

        return {
            "playback_controls": playback_controls,
            "speed_control": speed_control,
            "export_button": export_button,
            "reload_button": reload_button,
            "status_display": status_display,
        }
