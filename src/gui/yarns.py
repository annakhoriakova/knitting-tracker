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
    
    def create_header(self):
        """Create header with title and add button."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Yarns",
            font=FONTS['title']
        )
        title.grid(row=0, column=0, sticky="w")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="+ New Yarn",
            command=self.open_add_yarn,
            font=FONTS['button'],
            height=40,
            width=150
        )
        add_btn.grid(row=0, column=1, sticky="e")
    
    def create_yarns_list(self):
        """Create scrollable container for yarn cards."""
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.grid(row=1, column=0, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
    
    def load_yarns(self):
        """Load yarns from database."""
        # Clear existing items
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        # Get yarns
        self.yarns = self.tracker.get_all_yarns()
        
        if not self.yarns:
            empty_label = ctk.CTkLabel(
                self.list_frame,
                text="No yarns yet. Add your first yarn!",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            empty_label.grid(row=0, column=0, pady=20)
            return
        
        for i, yarn in enumerate(self.yarns):
            self.create_yarn_card(yarn, i)
    
    def create_yarn_card(self, yarn, index):
        """
        Create a yarn card with details and actions.
        
        Args:
            yarn: The yarn object to display
            index: The row index for grid positioning
        """
        card = ctk.CTkFrame(self.list_frame, corner_radius=15)
        card.grid(row=index, column=0, sticky="ew", pady=8)
        card.grid_columnconfigure(0, weight=1)
        
        # Main content
        content_frame = ctk.CTkFrame(card, fg_color="transparent")
        content_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Yarn brand and line
        brand_text = yarn.yarn_brand
        if yarn.yarn_line:
            brand_text += f" - {yarn.yarn_line}"
        
        brand_label = ctk.CTkLabel(
            content_frame,
            text=brand_text,
            font=FONTS['heading']
        )
        brand_label.grid(row=0, column=0, sticky="w")
        
        # Color
        if yarn.color_name:
            color_label = ctk.CTkLabel(
                content_frame,
                text=f"Color: {yarn.color_name}",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            color_label.grid(row=1, column=0, sticky="w", pady=(0, 5))
        
        # Details row
        details = []
        if yarn.weight_category:
            details.append(f"Weight: {yarn.weight_category}")
        if yarn.total_yardage:
            details.append(f"{yarn.total_yardage} yds")
        if yarn.dye_lot:
            details.append(f"Lot: {yarn.dye_lot}")
        
        details_text = " | ".join(details)
        if details_text:
            details_label = ctk.CTkLabel(
                content_frame,
                text=details_text,
                font=FONTS['body_small'],
                text_color=COLORS['text_secondary']
            )
            details_label.grid(row=2, column=0, sticky="w")
        
        # Count projects using this yarn
        # Get all projects and count usage
        projects = self.tracker.get_all_projects()
        usage_count = 0
        for project in projects:
            full_project = self.tracker.get_project(project.project_id)
            if full_project and full_project.yarns:
                usage_count += sum(1 for y in full_project.yarns if y['yarn_id'] == yarn.yarn_id)
        
        usage_label = ctk.CTkLabel(
            content_frame,
            text=f"Used in {usage_count} project{'s' if usage_count != 1 else ''}",
            font=FONTS['body_small'],
            text_color=COLORS['text_secondary']
        )
        usage_label.grid(row=3, column=0, sticky="w", pady=(5, 0))
        
        # Action buttons
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Edit",
            command=lambda: self.open_edit_yarn(yarn),
            width=80,
            font=FONTS['body_small']
        )
        edit_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Delete button (disabled if yarn is in use)
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Delete",
            command=lambda: self.delete_yarn(yarn),
            width=80,
            font=FONTS['body_small'],
            fg_color=COLORS['danger'] if usage_count == 0 else COLORS['text_disabled'],
            hover_color='#B71C1C' if usage_count == 0 else COLORS['text_disabled'],
            state="normal" if usage_count == 0 else "disabled"
        )
        delete_btn.grid(row=0, column=1, padx=(5, 0))
        
        if usage_count > 0:
            tooltip = ctk.CTkLabel(
                actions_frame,
                text="(in use: cannot delete)",
                font=FONTS['body_small'],
                text_color=COLORS['text_disabled']
            )
            tooltip.grid(row=0, column=2, padx=(10, 0))
    
    def open_add_yarn(self):
        """Open dialog to add a new yarn."""
        dialog = YarnDialog(self, self.tracker)
        self.wait_window(dialog)
        if dialog.result:
            self.load_yarns()
    
    def open_edit_yarn(self, yarn):
        """Open dialog to edit an existing yarn."""
        dialog = YarnDialog(self, self.tracker, yarn)
        self.wait_window(dialog)
        if dialog.result:
            self.load_yarns()
    
    def delete_yarn(self, yarn):
        """Delete a yarn with confirmation."""
        if messagebox.askyesno(
            "Delete Yarn",
            f"Are you sure you want to delete '{yarn.yarn_brand} {yarn.yarn_line or ''}'?\n"
            "This cannot be undone."
        ):
            try:
                self.tracker.delete_yarn(yarn.yarn_id)
                messagebox.showinfo("Success", "Yarn deleted successfully!")
                self.load_yarns()
            except Exception as e:
                if "FOREIGN KEY" in str(e):
                    messagebox.showerror(
                        "Error",
                        "Cannot delete this yarn because it is used in one or more projects."
                    )
                else:
                    messagebox.showerror("Error", f"Failed to delete yarn: {str(e)}")
                    