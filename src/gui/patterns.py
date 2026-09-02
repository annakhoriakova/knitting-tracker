"""
============================================================
Patterns Management View
============================================================
CRUD operations for patterns:
- List all patterns
- Create new patterns
- Edit existing patterns
- Delete patterns (with safety checks)

Author: Anna Khoriakova
Last Updated: 2026-09-02
============================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from src.crud import KnittingTracker
from src.models import Pattern
from src.gui.styles import COLORS, FONTS
from src.gui.dialogs import PatternDialog


class PatternsView(ctk.CTkFrame):
    """Patterns management view with CRUD operations."""
    
    def __init__(self, parent):
        super().__init__(parent, fg_color="transparent")
        
        self.tracker = KnittingTracker()
        self.patterns = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Build the view
        self.create_header()
        self.create_patterns_list()
        self.load_patterns()
    
    def create_header(self):
        """Create header with title and add button."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Patterns",
            font=FONTS['title']
        )
        title.grid(row=0, column=0, sticky="w")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="+ New Pattern",
            command=self.open_add_pattern,
            font=FONTS['button'],
            height=40,
            width=150
        )
        add_btn.grid(row=0, column=1, sticky="e")
    
    def create_patterns_list(self):
        """Create scrollable container for pattern cards."""
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.grid(row=1, column=0, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
    
    def load_patterns(self):
        """Load patterns from database."""
        # Clear existing items
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        # Get patterns
        self.patterns = self.tracker.get_all_patterns()
        
        if not self.patterns:
            empty_label = ctk.CTkLabel(
                self.list_frame,
                text="No patterns yet. Add your first pattern!",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            empty_label.grid(row=0, column=0, pady=20)
            return
        
        for i, pattern in enumerate(self.patterns):
            self.create_pattern_card(pattern, i)
    