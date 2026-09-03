"""
============================================================
Yarns Management View
============================================================
CRUD operations for yarns:
- List all yarns with details
- Create new yarns
- Edit existing yarns
- Delete yarns (with safety checks)

Author: Anna Khoriakova
Last Updated: 2026-09-02
============================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from src.crud import KnittingTracker
from src.models import Yarn
from src.gui.styles import COLORS, FONTS
from src.gui.dialogs import YarnDialog


class YarnsView(ctk.CTkFrame):
    """Yarns management view with CRUD operations."""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.tracker = KnittingTracker()
        self.yarns = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Build the view
        self.create_header()
        self.create_yarns_list()
        self.load_yarns()
    