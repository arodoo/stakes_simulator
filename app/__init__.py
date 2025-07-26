"""Application package."""


# Lazy import to avoid circular dependencies
def get_emulator_controller():
    """Get the EmulatorController class."""
    from .interface.controllers.emulator_controller import EmulatorController

    return EmulatorController


__all__ = ["get_emulator_controller"]
