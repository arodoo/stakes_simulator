"""Entry point for the vehicle emulator application."""

import tkinter as tk
from app.interface.controllers.emulator_controller import EmulatorController


def main():
    """Run the vehicle emulator application."""
    root = tk.Tk()
    app = EmulatorController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
