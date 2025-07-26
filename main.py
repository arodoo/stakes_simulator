"""
main.py
~~~~~~~

Entry point for the vehicle trajectory emulator.  This script simply
instantiates a Tkinter root window, constructs the
:class:`vehicle_emulator.app.EmulatorApp` and starts the Tkinter main 
loop.  It is designed to be run as a standalone program either via 
``python -m vehicle_emulator`` or directly as ``python vehicle_emulator/main.py``.  
When executed, it will connect to the database and load the required data
from the tables (``map``, ``bamboopattern``, ``centerpos2x`` and
``largescreenpixelpos``).
"""

from __future__ import annotations

import os
import sys
import argparse
import tkinter as tk

from .app import EmulatorApp


def main(argv: list[str] | None = None) -> None:
    """Run the emulator application.

    Parameters
    ----------
    argv: list[str], optional
        Command line arguments.  If ``None``, ``sys.argv`` will be
        used.
    """
    parser = argparse.ArgumentParser(description="Vehicle Trajectory Emulator")
    args = parser.parse_args(argv)
    root = tk.Tk()
    try:
        app = EmulatorApp(root)
    except Exception:
        # EmulatorApp already shows an error message; exit gracefully
        return
    root.mainloop()


if __name__ == '__main__':
    main()
