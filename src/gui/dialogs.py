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
Last Updated: 2026-09-01
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


# ============================================================
# NEEDLE DIALOG
# ============================================================

class NeedleDialog(BaseDialog):
    """Dialog for adding or editing a needle."""
    
    def __init__(self, parent, tracker, needle=None):
        self.tracker = tracker
        self.needle = needle
        title = "Edit Needle" if needle else "New Needle"
        super().__init__(parent, title, width=500, height=600)
        self.create_form()
        if needle:
            self.load_needle_data()
    
    def create_form(self):
        """Create the form fields."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Needle Size
        size_label = ctk.CTkLabel(main_frame, text="Needle Size (mm) *", font=FONTS['body'])
        size_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.size_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., 4.0")
        self.size_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Needle Type
        type_label = ctk.CTkLabel(main_frame, text="Needle Type *", font=FONTS['body'])
        type_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        self.type_menu = ctk.CTkOptionMenu(
            main_frame,
            values=NEEDLE_TYPES,
            width=200
        )
        self.type_menu.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self.type_menu.set("Select type...")
        
        # Needle Brand
        brand_label = ctk.CTkLabel(main_frame, text="Brand", font=FONTS['body'])
        brand_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        self.brand_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., KnitPro")
        self.brand_entry.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        
        # Needle Material
        material_label = ctk.CTkLabel(main_frame, text="Material", font=FONTS['body'])
        material_label.grid(row=6, column=0, sticky="w", pady=(0, 5))
        
        self.material_menu = ctk.CTkOptionMenu(
            main_frame,
            values=NEEDLE_MATERIALS,
            width=200
        )
        self.material_menu.grid(row=7, column=0, sticky="ew", pady=(0, 15))
        self.material_menu.set("Select material...")
        
        # Needle Length
        length_label = ctk.CTkLabel(main_frame, text="Length (inches)", font=FONTS['body'])
        length_label.grid(row=8, column=0, sticky="w", pady=(0, 5))
        
        self.length_menu = ctk.CTkOptionMenu(
            main_frame,
            values=NEEDLE_LENGTHS,
            width=200
        )
        self.length_menu.grid(row=9, column=0, sticky="ew", pady=(0, 20))
        self.length_menu.set("Select length...")
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=10, column=0, pady=(20, 0))
        
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
    
    def load_needle_data(self):
        """Load existing needle data into the form."""
        self.size_entry.insert(0, str(self.needle.needle_size_mm))
        self.type_menu.set(self.needle.needle_type)
        if self.needle.needle_brand:
            self.brand_entry.insert(0, self.needle.needle_brand)
        if self.needle.needle_material:
            self.material_menu.set(self.needle.needle_material)
        if self.needle.needle_length:
            self.length_menu.set(self.needle.needle_length)
    
    def save(self):
        """Save the needle data."""
        # Validate size
        size_text = self.size_entry.get().strip()
        if not size_text:
            messagebox.showerror("Error", "Needle size is required.")
            return
        
        try:
            size = float(size_text)
            if size <= 0:
                raise ValueError("Size must be positive")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid positive number for size.")
            return
        
        # Validate type
        needle_type = self.type_menu.get()
        if needle_type == "Select type...":
            messagebox.showerror("Error", "Please select a needle type.")
            return
        
        brand = self.brand_entry.get().strip() or None
        material = self.material_menu.get()
        if material == "Select material...":
            material = None
        
        length = self.length_menu.get()
        if length == "Select length...":
            length = None
        
        try:
            needle = Needle(
                needle_size_mm=size,
                needle_type=needle_type,
                needle_brand=brand,
                needle_material=material,
                needle_length=length
            )
            
            if self.needle:  # Editing
                self.tracker.update_needle(self.needle.needle_id, needle)
                messagebox.showinfo("Success", "Needle updated successfully!")
            else:  # New
                needle_id = self.tracker.create_needle(needle)
                messagebox.showinfo("Success", f"Needle created successfully!")
            
            self.result = True
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save needle: {str(e)}")


# ============================================================
# PROJECT DIALOG
# ============================================================

class ProjectDialog(BaseDialog):
    """Dialog for adding or editing a project."""
    
    def __init__(self, parent, tracker, project=None):
        self.tracker = tracker
        self.project = project
        title = "Edit Project" if project else "New Project"
        super().__init__(parent, title, width=600, height=700)
        
        self.create_form()
        if project:
            self.load_project_data()
    
    def create_form(self):
        """Create the form fields."""
        main_frame = ctk.CTkFrame(self, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # Project Name
        name_label = ctk.CTkLabel(main_frame, text="Project Name *", font=FONTS['body'])
        name_label.grid(row=0, column=0, sticky="w", pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., My Aran Sweater")
        self.name_entry.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Pattern selection
        pattern_label = ctk.CTkLabel(main_frame, text="Pattern *", font=FONTS['body'])
        pattern_label.grid(row=2, column=0, sticky="w", pady=(0, 5))
        
        patterns = self.tracker.get_all_patterns()
        pattern_names = [p.pattern_name for p in patterns]
        if not pattern_names:
            pattern_names = ["No patterns available - please add one first"]
        
        self.pattern_menu = ctk.CTkOptionMenu(
            main_frame,
            values=pattern_names,
            width=200
        )
        self.pattern_menu.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        self.patterns = patterns
        
        # Needle selection
        needle_label = ctk.CTkLabel(main_frame, text="Primary Needle *", font=FONTS['body'])
        needle_label.grid(row=4, column=0, sticky="w", pady=(0, 5))
        
        needles = self.tracker.get_all_needles()
        needle_names = [f"{n.needle_size_mm}mm {n.needle_type}" for n in needles]
        if not needle_names:
            needle_names = ["No needles available - please add one first"]
        
        self.needle_menu = ctk.CTkOptionMenu(
            main_frame,
            values=needle_names,
            width=200
        )
        self.needle_menu.grid(row=5, column=0, sticky="ew", pady=(0, 15))
        self.needles = needles
        
        # Status
        status_label = ctk.CTkLabel(main_frame, text="Status", font=FONTS['body'])
        status_label.grid(row=6, column=0, sticky="w", pady=(0, 5))
        
        self.status_menu = ctk.CTkOptionMenu(
            main_frame,
            values=STATUS_ORDER,
            width=200
        )
        self.status_menu.grid(row=7, column=0, sticky="ew", pady=(0, 15))
        self.status_menu.set("Planning")
        
        # Recipient
        recipient_label = ctk.CTkLabel(main_frame, text="Recipient", font=FONTS['body'])
        recipient_label.grid(row=8, column=0, sticky="w", pady=(0, 5))
        
        self.recipient_entry = ctk.CTkEntry(main_frame, placeholder_text="e.g., Me, Gift, or name")
        self.recipient_entry.grid(row=9, column=0, sticky="ew", pady=(0, 15))
        
        # Start Date
        self.start_date_auto = ctk.CTkCheckBox(
            main_frame,
            text="Start today",
            onvalue=True,
            offvalue=False
        )
        self.start_date_auto.grid(row=10, column=0, sticky="w", pady=(0, 5))
        self.start_date_auto.select()
        
        # Buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.grid(row=11, column=0, pady=(20, 0))
        
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
        
        # Configure grid
        main_frame.grid_columnconfigure(0, weight=1)
    
    def load_project_data(self):
        """Load existing project data into the form."""
        self.name_entry.insert(0, self.project.project_name)
        
        # Set pattern
        pattern = self.tracker.get_pattern(self.project.pattern_id)
        if pattern:
            try:
                self.pattern_menu.set(pattern.pattern_name)
            except:
                pass
        
        # Set needle
        needle = next(
            (n for n in self.needles if n.needle_id == self.project.needle_id),
            None
        )
        if needle:
            needle_text = f"{needle.needle_size_mm}mm {needle.needle_type}"
            try:
                self.needle_menu.set(needle_text)
            except:
                pass
        
        # Set status
        self.status_menu.set(self.project.status)
        
        # Set recipient
        if self.project.recipient:
            self.recipient_entry.insert(0, self.project.recipient)
        
        # Uncheck start date auto if there's a start date
        if self.project.start_date:
            self.start_date_auto.deselect()
    
    def save(self):
        """Save the project data."""
        # Validate required fields
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Project name is required.")
            return
        
        # Get selected pattern
        pattern_name = self.pattern_menu.get()
        if pattern_name == "No patterns available - please add one first" or not self.patterns:
            messagebox.showerror("Error", "Please add a pattern first.")
            return
        
        pattern = next((p for p in self.patterns if p.pattern_name == pattern_name), None)
        if not pattern:
            messagebox.showerror("Error", "Please select a valid pattern.")
            return
        
        # Get selected needle
        if not self.needles:
            messagebox.showerror("Error", "Please add a needle first.")
            return
        
        needle_text = self.needle_menu.get()
        if needle_text == "No needles available - please add one first":
            messagebox.showerror("Error", "Please add a needle first.")
            return
        
        needle = next(
            (n for n in self.needles if f"{n.needle_size_mm}mm {n.needle_type}" == needle_text),
            None
        )
        if not needle:
            messagebox.showerror("Error", "Please select a valid needle.")
            return
        
        # Get form data
        status = self.status_menu.get()
        recipient = self.recipient_entry.get().strip() or None
        
        # Get start date
        start_date = None
        if self.start_date_auto.get() == 1:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            project = Project(
                project_name=name,
                start_date=start_date,
                end_date=None if status != "Finished" else datetime.now().strftime("%Y-%m-%d"),
                status=status,
                recipient=recipient,
                pattern_id=pattern.pattern_id,
                needle_id=needle.needle_id
            )
            
            if self.project:  # Editing
                # Update status
                self.tracker.update_project_status(self.project.project_id, status)
                messagebox.showinfo("Success", "Project updated successfully!")
            else:  # New
                project_id = self.tracker.create_project(project)
                messagebox.showinfo("Success", f"Project created successfully!")
            
            self.result = True
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save project: {str(e)}")
            