"""
GUI Package for Knitting Tracker Application

This package contains all GUI components for the knitting tracker:
- Main window with navigation
- Dashboard with statistics
- CRUD views for projects, patterns, yarns, and needles
- Dialog windows for creating and editing records

Author: Anna Khoriakova
Last Updated: 2026-09-02
"""

from src.gui.main_window import MainWindow, run_app
from src.gui.styles import COLORS, FONTS, STATUS_COLORS, STATUS_DISPLAY

__all__ = [
    'MainWindow',
    'run_app',
    'COLORS',
    'FONTS',
    'STATUS_COLORS',
    'STATUS_DISPLAY'
]
