"""New main application entry point."""

import tkinter as tk


def main():
    """Main application entry point."""
    # Lazy import to avoid circular dependencies
    from app.interface.controllers.emulator_controller import EmulatorController
    
    root = tk.Tk()
    app = EmulatorController(root)
    root.mainloop()


if __name__ == "__main__":
    main()
