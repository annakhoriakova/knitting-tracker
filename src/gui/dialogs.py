"""
============================================================
Dialog Windows
============================================================
This module contains dialog windows for:
- Creating and editing projects
- Creating and editing patterns
- Creating and editing yarns
- Creating and editing needles

Author: Anna Khoriakova
Last Updated: 2026-08-30
============================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from src.models import Project, Pattern, Needle, Yarn
from src.gui.styles import (
    FONTS, STATUS_ORDER, YARN_WEIGHTS, 
    NEEDLE_TYPES, NEEDLE_MATERIALS, NEEDLE_LENGTHS
)


class BaseDialog(ctk.CTkToplevel):
    """Base class for all dialog windows."""
    
    def __init__(self, parent, title, width=500, height=600):
        super().__init__(parent)
        
        self.result = False
        
        # Window setup
        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)
        
        # Make it modal
        self.transient(parent)
        self.grab_set()
        
        # Center on parent
        self.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - height) // 2
        self.geometry(f"+{x}+{y}")
    
    def cancel(self):
        """Cancel and close the dialog."""
        self.result = False
        self.destroy()
