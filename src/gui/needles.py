"""
============================================================
Needles Management View
============================================================
CRUD operations for needles:
- List all needles with details
- Create new needles
- Edit existing needles
- Delete needles (with safety checks)

Author: Anna Khoriakova
Last Updated: 2026-09-01
============================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from src.crud import KnittingTracker
from src.models import Needle
from src.gui.styles import COLORS, FONTS
from src.gui.dialogs import NeedleDialog


class NeedlesView(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.tracker = KnittingTracker()
        self.needles = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Build the view
        self.create_header()
        self.create_needles_list()
        self.load_needles()
    