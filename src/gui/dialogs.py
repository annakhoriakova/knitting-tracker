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


# ============================================================
# PATTERN DIALOG
# ============================================================

class PatternDialog(BaseDialog):
    """Dialog for adding or editing a pattern."""
    
    def __init__(self, parent, tracker, pattern=None):
        self.tracker = tracker
        self.pattern = pattern
        title = "Edit Pattern" if pattern else "New Pattern"
        super().__init__(parent, title, width=500, height=300)
        self.create_form()
        if pattern:
            self.load_pattern_data()
    
    def create_form(self):
        """Create the form fields."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Pattern Name
        name_label = ctk.CTkLabel(main_frame, text="Pattern Name *", font=FONTS['body'])
        name_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., Aran Sweater")
        self.name_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Designer
        designer_label = ctk.CTkLabel(main_frame, text="Designer", font=FONTS['body'])
        designer_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.designer_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., Alice Starmore")
        self.designer_entry.grid(row=3, column=0, sticky="ew", pady=(0, 20))
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=4, column=0, pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.cancel,
            width=100
        )
        cancel_btn.grid(row=0, column=0, padx=5)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=self.save,
            width=100
        )
        save_btn.grid(row=0, column=1, padx=5)
        
        main_frame.grid_columnconfigure(0, weight=1)
    
    def load_pattern_data(self):
        """Load existing pattern data into the form."""
        self.name_entry.insert(0, self.pattern.pattern_name)
        if self.pattern.designer:
            self.designer_entry.insert(0, self.pattern.designer)
    
    def save(self):
        """Save the pattern data."""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Pattern name is required.")
            return
        
        designer = self.designer_entry.get().strip() or None
        
        try:
            pattern = Pattern(pattern_name=name, designer=designer)
            
            if self.pattern:  # Editing
                self.tracker.update_pattern(self.pattern.pattern_id, pattern)
                messagebox.showinfo("Success", "Pattern updated successfully!")
            else:  # New
                pattern_id = self.tracker.create_pattern(pattern)
                messagebox.showinfo("Success", f"Pattern created successfully!")
            
            self.result = True
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save pattern: {str(e)}")


# ============================================================
# YARN DIALOG
# ============================================================

class YarnDialog(BaseDialog):
    """Dialog for adding or editing a yarn."""
    
    def __init__(self, parent, tracker, yarn=None):
        self.tracker = tracker
        self.yarn = yarn
        title = "Edit Yarn" if yarn else "New Yarn"
        super().__init__(parent, title, width=600, height=650)
        self.create_form()
        if yarn:
            self.load_yarn_data()
    
    def create_form(self):
        """Create the form fields."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Yarn Brand
        brand_label = ctk.CTkLabel(main_frame, text="Brand *", font=FONTS['body'])
        brand_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.brand_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., Malabrigo")
        self.brand_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Yarn Line
        line_label = ctk.CTkLabel(main_frame, text="Line/Product Name", font=FONTS['body'])
        line_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.line_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., Rios")
        self.line_entry.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        
        # Colour Name
        colour_label = ctk.CTkLabel(main_frame, text="Colour Name", font=FONTS['body'])
        colour_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.colour_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., Whale's Road")
        self.colour_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        
        # Weight Category
        weight_label = ctk.CTkLabel(main_frame, text="Weight Category", font=FONTS['body'])
        weight_label.grid(row=6, column=0, sticky="w", pady=(0, 5))
        
        self.weight_menu = ctk.CTkOptionMenu(
            main_frame,
            values=YARN_WEIGHTS,
            width=200
        )
        self.weight_menu.grid(row=7, column=0, sticky="ew", pady=(0, 15))
        self.weight_menu.set("Select weight...")
        
        # Total Yardage
        yardage_label = ctk.CTkLabel(main_frame, text="Total Yardage (yards per skein)", font=FONTS['body'])
        yardage_label.grid(row=8, column=0, sticky="w", pady=(0, 5))
        
        self.yardage_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., 210")
        self.yardage_entry.grid(row=9, column=0, sticky="ew", pady=(0, 15))
        
        # Dye Lot
        dyelot_label = ctk.CTkLabel(main_frame, text="Dye Lot", font=FONTS['body'])
        dyelot_label.grid(row=10, column=0, sticky="w", pady=(0, 5))
        
        self.dyelot_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., 12345")
        self.dyelot_entry.grid(row=11, column=0, sticky="ew", pady=(0, 20))
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=12, column=0, pady=(20, 0))
        
        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=self.cancel,
            width=100
        )
        cancel_btn.grid(row=0, column=0, padx=5)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="Save",
            command=self.save,
            width=100
        )
        save_btn.grid(row=0, column=1, padx=5)
        
        main_frame.grid_columnconfigure(0, weight=1)
    
    def load_yarn_data(self):
        """Load existing yarn data into the form."""
        self.brand_entry.insert(0, self.yarn.yarn_brand)
        if self.yarn.yarn_line:
            self.line_entry.insert(0, self.yarn.yarn_line)
        if self.yarn.colour_name:
            self.colour_entry.insert(0, self.yarn.colour_name)
        if self.yarn.weight_category:
            self.weight_menu.set(self.yarn.weight_category)
        if self.yarn.total_yardage:
            self.yardage_entry.insert(0, str(self.yarn.total_yardage))
        if self.yarn.dye_lot:
            self.dyelot_entry.insert(0, self.yarn.dye_lot)
    
    def save(self):
        """Save the yarn data."""
        brand = self.brand_entry.get().strip()
        if not brand:
            messagebox.showerror("Error", "Yarn brand is required.")
            return
        
        line = self.line_entry.get().strip() or None
        colour = self.colour_entry.get().strip() or None
        weight = self.weight_menu.get()
        if weight == "Select weight...":
            weight = None
        
        yardage_text = self.yardage_entry.get().strip()
        yardage = None
        if yardage_text:
            try:
                yardage = int(yardage_text)
                if yardage <= 0:
                    raise ValueError("Yardage must be positive")
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid positive number for yardage.")
                return
        
        dye_lot = self.dyelot_entry.get().strip() or None
        
        try:
            yarn = Yarn(
                yarn_brand=brand,
                yarn_line=line,
                colour_name=colour,
                weight_category=weight,
                total_yardage=yardage,
                dye_lot=dye_lot
            )
            
            if self.yarn:  # Editing
                self.tracker.update_yarn(self.yarn.yarn_id, yarn)
                messagebox.showinfo("Success", "Yarn updated successfully!")
            else:  # New
                yarn_id = self.tracker.create_yarn(yarn)
                messagebox.showinfo("Success", f"Yarn created successfully!")
            
            self.result = True
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save yarn: {str(e)}")
