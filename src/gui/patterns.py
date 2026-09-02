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
    
    def create_pattern_card(self, pattern, index):
        """
        Create a pattern card with details and actions.
        
        Args:
            pattern: The pattern object to display
            index: The row index for grid positioning
        """
        card = ctk.CTkFrame(self.list_frame, corner_radius=15)
        card.grid(row=index, column=0, sticky="ew", pady=8)
        card.grid_columnconfigure(0, weight=1)
        
        # Main content
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Pattern name
        name_label = ctk.CTkLabel(
            content_frame,
            text=pattern.pattern_name,
            font=FONTS['heading']
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        # Designer
        if pattern.designer:
            designer_label = ctk.CTkLabel(
                content_frame,
                text=f"by {pattern.designer}",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            designer_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        # Count projects using this pattern
        projects = self.tracker.get_all_projects()
        project_count = sum(1 for p in projects if p.pattern_id == pattern.pattern_id)
        
        usage_label = ctk.CTkLabel(
            content_frame,
            text=f"Used in {project_count} project{'s' if project_count != 1 else ''}",
            font=FONTS['body_small'],
            text_color=COLORS['text_secondary']
        )
        usage_label.grid(row=2, column=0, sticky="w")
        
        # Action buttons
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Edit",
            command=lambda: self.open_edit_pattern(pattern),
            width=80,
            font=FONTS['body_small']
        )
        edit_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Delete button (disabled if pattern is in use)
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Delete",
            command=lambda: self.delete_pattern(pattern),
            width=80,
            font=FONTS['body_small'],
            fg_color=COLORS['danger'] if project_count == 0 else COLORS['text_disabled'],
            hover_color='#B71C1C' if project_count == 0 else COLORS['text_disabled'],
            state="normal" if project_count == 0 else "disabled"
        )
        delete_btn.grid(row=0, column=1, padx=(5, 0))
        
        if project_count > 0:
            # Add tooltip-like explanation
            tooltip = ctk.CTkLabel(
                actions_frame,
                text="(in use: cannot delete)",
                font=FONTS['body_small'],
                text_color=COLORS['text_disabled']
            )
            tooltip.grid(row=0, column=2, padx=(10, 0))
    
    def open_add_pattern(self):
        """Open dialog to add a new pattern."""
        dialog = PatternDialog(self, self.tracker)
        self.wait_window(dialog)
        if dialog.result:
            self.load_patterns()
    
    def open_edit_pattern(self, pattern):
        """Open dialog to edit an existing pattern."""
        dialog = PatternDialog(self, self.tracker, pattern)
        self.wait_window(dialog)
        if dialog.result:
            self.load_patterns()
    
    def delete_pattern(self, pattern):
        """Delete a pattern with confirmation."""
        if messagebox.askyesno(
            "Delete Pattern",
            f"Are you sure you want to delete '{pattern.pattern_name}'?\n"
            "This cannot be undone."
        ):
            try:
                self.tracker.delete_pattern(pattern.pattern_id)
                messagebox.showinfo("Success", f"Pattern '{pattern.pattern_name}' deleted successfully!")
                self.load_patterns()
            except Exception as e:
                if "FOREIGN KEY" in str(e):
                    messagebox.showerror(
                        "Error",
                        f"Cannot delete '{pattern.pattern_name}' because it is used in one or more projects."
                    )
                else:
                    messagebox.showerror("Error", f"Failed to delete pattern: {str(e)}")
                    