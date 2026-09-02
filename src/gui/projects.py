"""
============================================================
Projects Management View
============================================================
This view provides CRUD operations for projects:
- List all projects with filtering by status
- Create new projects
- Edit existing projects
- Update project status
- Delete projects

Author: Anna Khoriakova
Last Updated: 2026-09-02
============================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from src.crud import KnittingTracker
from src.models import Project
from src.gui.styles import (
    COLORS, FONTS, STATUS_ORDER,
    get_status_color, get_status_display
)
from src.gui.dialogs import ProjectDialog
