# Vehicle Emulator package

"""
The vehicle_emulator package contains all of the classes and functions
required to load a set of Excel based map files, visualise the
corresponding trajectories on a series of canvases and interactively
calibrate individual points.  It is designed to be robust and
re-usable: data loading, coordinate scaling and persistence are
encapsulated inside dedicated classes and functions to allow the rest
of the application to focus solely on user interaction and rendering.

Modules
-------

data_manager
    Contains the ``DataManager`` class responsible for loading and
    exposing trajectory information.  This module also implements the
    export logic for writing calibrated data back to new Excel files.

view_canvas
    Defines the ``ViewCanvas`` widget which wraps a Tkinter ``Canvas``
    to draw the trajectory and vehicle marker for a given dataset.
    It provides helper functions for coordinate conversion and user
    interaction to adjust individual points.

app
    Houses the ``EmulatorApp`` class which wires together the
    data manager, canvases and controls.  It implements playback,
    navigation and user interface logic.
"""
