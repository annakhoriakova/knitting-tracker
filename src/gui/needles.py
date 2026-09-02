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
    """Needles management view with CRUD operations."""
    
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
    
    def create_header(self):
        """Create header with title and add button."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Needles",
            font=FONTS['title']
        )
        title.grid(row=0, column=0, sticky="w")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="+ New Needle",
            command=self.open_add_needle,
            font=FONTS['button'],
            height=40,
            width=150
        )
        add_btn.grid(row=0, column=1, sticky="e")
    
    def create_needles_list(self):
        """Create scrollable container for needle cards."""
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.grid(row=1, column=0, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
    
    def load_needles(self):
        """Load needles from database."""
        # Clear existing items
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        # Get needles
        self.needles = self.tracker.get_all_needles()
        
        if not self.needles:
            empty_label = ctk.CTkLabel(
                self.list_frame,
                text="No needles yet. Add your first needle!",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            empty_label.grid(row=0, column=0, pady=20)
            return
        
        for i, needle in enumerate(self.needles):
            self.create_needle_card(needle, i)
    
    def create_needle_card(self, needle, index):
        """
        Create a needle card with details and actions.
        
        Args:
            needle: The needle object to display
            index: The row index for grid positioning
        """
        card = ctk.CTkFrame(self.list_frame, corner_radius=15)
        card.grid(row=index, column=0, sticky="ew", pady=8)
        card.grid_columnconfigure(0, weight=1)
        
        # Main content
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Size and type
        size_type_text = f"{needle.needle_size_mm}mm {needle.needle_type}"
        size_label = ctk.CTkLabel(
            content_frame,
            text=size_type_text,
            font=FONTS['heading']
        )
        size_label.grid(row=0, column=0, sticky="w")
        
        # Details row
        details = []
        if needle.needle_brand:
            details.append(f"Brand: {needle.needle_brand}")
        if needle.needle_material:
            details.append(f"Material: {needle.needle_material}")
        if needle.needle_length:
            details.append(f"Length: {needle.needle_length}\"")
        
        details_text = " | ".join(details)
        if details_text:
            details_label = ctk.CTkLabel(
                content_frame,
                text=details_text,
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            details_label.grid(row=1, column=0, sticky="w", pady=(5, 0))
        
        # Count projects using this needle
        projects = self.tracker.get_all_projects()
        project_count = sum(1 for p in projects if p.needle_id == needle.needle_id)
        
        usage_label = ctk.CTkLabel(
            content_frame,
            text=f"Used in {project_count} project{'s' if project_count != 1 else ''}",
            font=FONTS['body_small'],
            text_color=COLORS['text_secondary']
        )
        usage_label.grid(row=2, column=0, sticky="w", pady=(5, 0))
        
        # Action buttons
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Edit",
            command=lambda: self.open_edit_needle(needle),
            width=80,
            font=FONTS['body_small']
        )
        edit_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Delete button (disabled if needle is in use)
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Delete",
            command=lambda: self.delete_needle(needle),
            width=80,
            font=FONTS['body_small'],
            fg_color=COLORS['danger'] if project_count == 0 else COLORS['text_disabled'],
            hover_color='#B71C1C' if project_count == 0 else COLORS['text_disabled'],
            state="normal" if project_count == 0 else "disabled"
        )
        delete_btn.grid(row=0, column=1, padx=(5, 0))
        
        if project_count > 0:
            tooltip = ctk.CTkLabel(
                actions_frame,
                text="(in use - cannot delete)",
                font=FONTS['body_small'],
                text_color=COLORS['text_disabled']
            )
            tooltip.grid(row=0, column=2, padx=(10, 0))
    
    def open_add_needle(self):
        """Open dialog to add a new needle."""
        dialog = NeedleDialog(self, self.tracker)
        self.wait_window(dialog)
        if dialog.result:
            self.load_needles()
    
    def open_edit_needle(self, needle):
        """Open dialog to edit an existing needle."""
        dialog = NeedleDialog(self, self.tracker, needle)
        self.wait_window(dialog)
        if dialog.result:
            self.load_needles()
    
    def delete_needle(self, needle):
        """Delete a needle with confirmation."""
        if messagebox.askyesno(
            "Delete Needle",
            f"Are you sure you want to delete the {needle.needle_size_mm}mm {needle.needle_type} needle?\n"
            "This cannot be undone."
        ):
            try:
                self.tracker.delete_needle(needle.needle_id)
                messagebox.showinfo("Success", "Needle deleted successfully!")
                self.load_needles()
            except Exception as e:
                if "FOREIGN KEY" in str(e):
                    messagebox.showerror(
                        "Error",
                        "Cannot delete this needle because it is used in one or more projects."
                    )
                else:
                    messagebox.showerror("Error", f"Failed to delete needle: {str(e)}")
                    