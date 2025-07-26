"""Vehicle Emulator Package.

A modular vehicle trajectory emulator built with Domain-Driven Design principles.

The vehicle_emulator package provides a clean separation of concerns:
- Domain layer: Core business logic (entities, value objects, domain services)
- Application layer: Use cases and application services
- Infrastructure layer: Database access, file I/O, external services
- Interface layer: User interface components and controllers

The application loads Excel-based map files, visualizes trajectories
on multiple canvases, and allows interactive calibration of individual points.
"""

from .app import EmulatorController

__version__ = "2.0.0"
__all__ = ["EmulatorController"]
