"""Control panel widgets for the emulator."""

from __future__ import annotations

import tkinter as tk
from tkinter import ttk
from typing import Optional, Callable


class PlaybackControls:
    """Playback control widgets."""

    def __init__(self, parent: tk.Widget, callbacks: dict[str, Callable]):
        """Initialize playback controls."""
        self.parent = parent
        self.callbacks = callbacks
        self._create_widgets()

    def _create_widgets(self) -> None:
        """Create playback control widgets."""
        self.play_button = ttk.Button(
            self.parent, text="Play", command=self.callbacks.get("toggle_play")
        )
        self.play_button.pack(side=tk.LEFT, padx=2)

        self.step_back_button = ttk.Button(
            self.parent, text="Back", command=self.callbacks.get("step_back")
        )
        self.step_back_button.pack(side=tk.LEFT, padx=2)

        self.step_forward_button = ttk.Button(
            self.parent, text="Forward", command=self.callbacks.get("step_forward")
        )
        self.step_forward_button.pack(side=tk.LEFT, padx=2)

        self.reset_button = ttk.Button(
            self.parent, text="Reset", command=self.callbacks.get("reset")
        )
        self.reset_button.pack(side=tk.LEFT, padx=2)

    def set_play_text(self, text: str) -> None:
        """Set the play button text."""
        self.play_button.config(text=text)

    def set_callbacks(self, callbacks: dict[str, Callable]) -> None:
        """Update callbacks for buttons."""
        self.callbacks.update(callbacks)
        self.play_button.config(command=self.callbacks.get("toggle_play"))
        self.step_back_button.config(command=self.callbacks.get("step_back"))
        self.step_forward_button.config(command=self.callbacks.get("step_forward"))
        self.reset_button.config(command=self.callbacks.get("reset"))
