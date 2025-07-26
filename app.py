"""
app.py
~~~~~~

This module defines the :class:`EmulatorApp` which provides a user
interface for visualising the trajectories of multiple vehicles across
three views.  It uses Tkinter to build a simple window containing
three canvases (one for each view) and a control panel with buttons
and sliders for playback and calibration.

Core Features
-------------
* Play/pause the animation with adjustable speed.
* Step forwards/backwards through the trajectory one record at a
  time.
* Reset to the beginning of the dataset.
* Drag the vehicle marker in any view to calibrate that point.
* Export all calibrated data to Excel files via a dedicated button.

The class is self‑contained and depends on
:class:`vehicle_emulator.data_manager.DataManager` for data access and
:class:`vehicle_emulator.view_canvas.ViewCanvas` for rendering.
"""

from __future__ import annotations

import os
import tkinter as tk
from tkinter import ttk, filedialog
from typing import Optional

from .data_manager import DataManager
from .view_canvas import ViewCanvas


class EmulatorApp:
    """Main application class for the vehicle emulator."""

    def __init__(self, root: tk.Tk, data_dir: str) -> None:
        self.root = root
        self.root.title("Vehicle Trajectory Emulator")
        # Attempt to load data
        try:
            self.data_manager = DataManager(data_dir)
        except Exception as exc:
            print(f"ERROR: Failed to initialise data: {exc}")
            # If data cannot be loaded there is no point continuing
            raise
        # Playback state
        self.current_index: int = 0
        self.playing: bool = False
        self.speed_step: int = 1  # number of records to advance per tick
        # Build UI
        self._build_ui()
        self._update_all_views()

    def _build_ui(self) -> None:
        """Assemble the main window layout and widgets."""
        # Frames for views
        view_frame = ttk.Frame(self.root)
        view_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        # Create canvases for each view
        self.canvases: dict[str, ViewCanvas] = {}
        view_names = ['bamboopattern', 'centerpos2x', 'largescreenpixelpos']
        for i, view_name in enumerate(view_names):
            frame = ttk.Frame(view_frame, relief=tk.SUNKEN, borderwidth=1)
            frame.grid(row=0, column=i, padx=5, pady=5, sticky='nsew')
            view_frame.columnconfigure(i, weight=1)
            label = ttk.Label(frame, text=view_name.capitalize())
            label.pack(side=tk.TOP, pady=(2, 2))
            canvas = ViewCanvas(frame, self.data_manager, view_name,
                                width=400, height=300)
            canvas.pack(fill=tk.BOTH, expand=True)
            self.canvases[view_name] = canvas
        # Control panel
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        # Buttons
        self.play_button = ttk.Button(control_frame, text="Play", command=self.toggle_play)
        self.play_button.pack(side=tk.LEFT, padx=2)
        self.step_back_button = ttk.Button(control_frame, text="Back", command=self.step_back)
        self.step_back_button.pack(side=tk.LEFT, padx=2)
        self.step_forward_button = ttk.Button(control_frame, text="Forward", command=self.step_forward)
        self.step_forward_button.pack(side=tk.LEFT, padx=2)
        self.reset_button = ttk.Button(control_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.LEFT, padx=2)
        # Speed slider
        speed_label = ttk.Label(control_frame, text="Speed (records per tick):")
        speed_label.pack(side=tk.LEFT, padx=(20, 2))
        self.speed_var = tk.IntVar(value=1)
        speed_slider = ttk.Scale(control_frame, from_=1, to=20, orient=tk.HORIZONTAL,
                                 variable=self.speed_var, command=self._on_speed_change)
        speed_slider.pack(side=tk.LEFT, padx=2)
        # Export button
        self.export_button = ttk.Button(control_frame, text="Export Calibrated", command=self.export_data)
        self.export_button.pack(side=tk.RIGHT, padx=2)
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(control_frame, textvariable=self.status_var)
        status_label.pack(side=tk.RIGHT, padx=(2, 10))

    def _on_speed_change(self, event: Optional[str] = None) -> None:
        """Callback when the speed slider changes."""
        value = self.speed_var.get()
        self.speed_step = max(1, int(value))
        if self.playing:
            # Immediately reflect new speed on next tick
            self.status_var.set(f"Speed set to {self.speed_step}")

    def toggle_play(self) -> None:
        """Toggle between play and pause states."""
        self.playing = not self.playing
        if self.playing:
            self.play_button.config(text="Pause")
            self.status_var.set("Playing")
            self._schedule_next_tick()
        else:
            self.play_button.config(text="Play")
            self.status_var.set("Paused")

    def _schedule_next_tick(self) -> None:
        """Schedule the next playback update when playing."""
        if self.playing:
            self.root.after(100, self._tick)  # 100 ms interval (~10 fps)

    def _tick(self) -> None:
        """Advance the playback and update the UI."""
        if not self.playing:
            return
        self.current_index += self.speed_step
        if self.current_index >= self.data_manager.total_records:
            # Stop at the end
            self.current_index = self.data_manager.total_records - 1
            self.playing = False
            self.play_button.config(text="Play")
            self.status_var.set("Reached end of data")
        self._update_all_views()
        self._schedule_next_tick()

    def step_forward(self) -> None:
        """Step the current index forward by one and update views."""
        if self.current_index < self.data_manager.total_records - 1:
            self.current_index += 1
            self._update_all_views()
            self.status_var.set(f"Index: {self.current_index}")
        else:
            self.status_var.set("Already at end")

    def step_back(self) -> None:
        """Step the current index backward by one and update views."""
        if self.current_index > 0:
            self.current_index -= 1
            self._update_all_views()
            self.status_var.set(f"Index: {self.current_index}")
        else:
            self.status_var.set("Already at beginning")

    def reset(self) -> None:
        """Reset playback to the start."""
        self.current_index = 0
        self.playing = False
        self.play_button.config(text="Play")
        self._update_all_views()
        self.status_var.set("Reset to start")

    def _update_all_views(self) -> None:
        """Refresh marker positions on all canvases."""
        for view_name, canvas in self.canvases.items():
            canvas.update_marker(self.current_index)

    def export_data(self) -> None:
        """Prompt the user for an output directory and export calibrated data."""
        output_dir = filedialog.askdirectory(title="Select output directory for calibrated files")
        if not output_dir:
            return  # User cancelled
        try:
            written = self.data_manager.export_calibrated(output_dir)
        except Exception as exc:
            print(f"ERROR: Failed to export calibrated data: {exc}")
            return
        msg_lines = ["Calibrated files written:"]
        for view, path in written.items():
            msg_lines.append(f"  {view}: {os.path.basename(path)}")
        print("\n".join(msg_lines))
