"""
main.py
~~~~~~~

Entry point for the vehicle trajectory emulator.  This script simply
instantiates a Tkinter root window, constructs the
:class:`vehicle_emulator.app.EmulatorApp` around the provided data
directory and starts the Tkinter main loop.  It is designed to be run
as a standalone program either via ``python -m vehicle_emulator`` or
directly as ``python vehicle_emulator/main.py``.  When executed, it
will look for the required Excel files (``map.xlsx``,
``bamboopattern.xlsx``, ``centerpos2x.xlsx`` and
``largescreenpixelpos.xlsx``) in the same directory as this script by
default.  An alternative data directory can be supplied on the
command line.
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
    parser.add_argument(
        'data_dir', nargs='?', default=os.path.join(os.path.dirname(__file__), 'share'),
        help=("Directory containing map.xlsx, bamboopattern.xlsx, "
              "centerpos2x.xlsx and largescreenpixelpos.xlsx. If not "
              "specified, the directory 'share' relative to the "
              "package location is used.")
    )
    args = parser.parse_args(argv)
    root = tk.Tk()
    # Expand tilde and environment variables
    data_dir = os.path.expanduser(os.path.expandvars(args.data_dir))
    try:
        app = EmulatorApp(root, data_dir)
    except Exception:
        # EmulatorApp already shows an error message; exit gracefully
        return
    root.mainloop()


if __name__ == '__main__':
    main()
