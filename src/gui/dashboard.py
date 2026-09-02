"""
============================================================
Dashboard View
============================================================
The dashboard provides an overview of the knitting tracker:
- Statistics cards (total projects, WIP, finished, patterns)
- Recent projects list
- Quick status overview

Author: Anna Khoriakova
Last Updated: 2026-09-01
============================================================
"""

import customtkinter as ctk
from src.crud import KnittingTracker
from src.gui.styles import COLORS, FONTS, get_status_color, get_status_display


class DashboardView(ctk.CTkFrame):
    """
    Dashboard showing project statistics and recent activity.
    
    This view provides a high-level overview of all knitting projects
    with visual statistics and a list of recent projects.
    """
            