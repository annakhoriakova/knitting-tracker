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


class ProjectsView(ctk.CTkFrame):
    """
    Main projects management view.
    
    This view displays all projects in a scrollable list with:
    - Filter dropdown for status
    - Add/Edit/Delete buttons
    - Status update dropdown for each project
    """
    
    def __init__(self, parent):
        """Initialize the projects view."""
        super().__init__(parent, fg_color="transparent")
        
        self.tracker = KnittingTracker()
        self.projects = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Build the view
        self.create_header()
        self.create_filter_bar()
        self.create_projects_list()
        self.load_projects()
    
    def create_header(self):
        """Create header with title and add button."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        header_frame.grid_columnconfigure(0, weight=1)
        
        title = ctk.CTkLabel(
            header_frame,
            text="Your Projects",
            font=FONTS['title']
        )
        title.grid(row=0, column=0, sticky="w")
        
        add_btn = ctk.CTkButton(
            header_frame,
            text="+ New Project",
            command=self.open_add_project,
            font=FONTS['button'],
            height=40,
            width=150
        )
        add_btn.grid(row=0, column=1, sticky="e")
    
    def create_filter_bar(self):
        """Create filter bar with status dropdown and refresh button."""
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        
        # Status filter label
        status_label = ctk.CTkLabel(
            filter_frame,
            text="Filter by status:",
            font=FONTS['body']
        )
        status_label.grid(row=0, column=0, padx=(0, 10))
        
        # Status filter dropdown
        self.status_filter = ctk.CTkOptionMenu(
            filter_frame,
            values=["All"] + STATUS_ORDER,
            command=self.on_filter_changed,
            width=150
        )
        self.status_filter.grid(row=0, column=1, padx=(0, 20))
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            filter_frame,
            text="Refresh",
            command=self.load_projects,
            width=100,
            font=FONTS['body_small']
        )
        refresh_btn.grid(row=0, column=2, sticky="e")
    
    def create_projects_list(self):
        """Create scrollable container for project cards."""
        self.list_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.list_frame.grid(row=2, column=0, sticky="nsew")
        self.list_frame.grid_columnconfigure(0, weight=1)
    
    def load_projects(self):
        """Load projects from database with current filter applied."""
        # Clear existing items
        for widget in self.list_frame.winfo_children():
            widget.destroy()
        
        # Get all projects
        all_projects = self.tracker.get_all_projects()
        
        # Apply status filter
        filter_status = self.status_filter.get()
        if filter_status != "All":
            self.projects = [p for p in all_projects if p.status == filter_status]
        else:
            self.projects = all_projects
        
        # Show empty state if no projects
        if not self.projects:
            empty_label = ctk.CTkLabel(
                self.list_frame,
                text="No projects found. Create your first project!",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            empty_label.grid(row=0, column=0, pady=20)
            return
        
        # Create project cards
        for i, project in enumerate(self.projects):
            self.create_project_card(project, i)
    
    def create_project_card(self, project, index):
        """
        Create a project card with all details and actions.
        
        Args:
            project: The project object to display
            index: The row index for grid positioning
        """
        card = ctk.CTkFrame(self.list_frame, corner_radius=15)
        card.grid(row=index, column=0, sticky="ew", pady=8)
        card.grid_columnconfigure(0, weight=1)
        
        # Top row: Name and status
        top_frame = ctk.CTkFrame(card, fg_color="transparent")
        top_frame.grid(row=0, column=0, sticky="ew", padx=15, pady=(10, 5))
        top_frame.grid_columnconfigure(0, weight=1)
        
        name_label = ctk.CTkLabel(
            top_frame,
            text=project.project_name,
            font=FONTS['heading']
        )
        name_label.grid(row=0, column=0, sticky="w")
        
        status_display = get_status_display(project.status)
        status_color = get_status_color(project.status)
        
        status_label = ctk.CTkLabel(
            top_frame,
            text=status_display,
            font=FONTS['body'],
            text_color=status_color
        )
        status_label.grid(row=0, column=1, padx=(10, 0))
        
        # Middle row: Details
        details_frame = ctk.CTkFrame(card, fg_color="transparent")
        details_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=5)
        
        details = []
        if project.start_date:
            details.append(f"Started: {project.start_date}")
        if project.end_date:
            details.append(f"Finished: {project.end_date}")
        if project.recipient:
            details.append(f"{project.recipient}")
        
        # Get pattern name
        pattern = self.tracker.get_pattern(project.pattern_id)
        if pattern:
            details.append(f"{pattern.pattern_name}")
        
        # Get yarns
        project_with_yarns = self.tracker.get_project(project.project_id)
        if project_with_yarns and project_with_yarns.yarns:
            yarn_names = [y['yarn_brand'] for y in project_with_yarns.yarns[:3]]
            details.append(f"{', '.join(yarn_names)}")
        
        details_text = " | ".join(details)
        details_label = ctk.CTkLabel(
            details_frame,
            text=details_text,
            font=FONTS['body_small'],
            text_color=COLORS['text_secondary']
        )
        details_label.grid(row=0, column=0, sticky="w")
        
        # Bottom row: Action buttons
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=(5, 10))
        
        # Edit button
        edit_btn = ctk.CTkButton(
            actions_frame,
            text="Edit",
            command=lambda: self.open_edit_project(project),
            width=80,
            font=FONTS['body_small']
        )
        edit_btn.grid(row=0, column=0, padx=(0, 5))
        
        # Status update dropdown
        status_menu = ctk.CTkOptionMenu(
            actions_frame,
            values=STATUS_ORDER,
            command=lambda status, p=project: self.update_status(p, status),
            width=120,
            font=FONTS['body_small']
        )
        status_menu.set(project.status)
        status_menu.grid(row=0, column=1, padx=5)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            actions_frame,
            text="Delete",
            command=lambda: self.delete_project(project),
            width=80,
            font=FONTS['body_small'],
            fg_color=COLORS['danger'],
            hover_color='#B71C1C'
        )
        delete_btn.grid(row=0, column=2, padx=(5, 0))
    
    def on_filter_changed(self, choice):
        """Handle filter dropdown changes."""
        self.load_projects()
    
    def open_add_project(self):
        """Open dialog to add a new project."""
        dialog = ProjectDialog(self, self.tracker)
        self.wait_window(dialog)
        if dialog.result:
            self.load_projects()
    
    def open_edit_project(self, project):
        """Open dialog to edit an existing project."""
        dialog = ProjectDialog(self, self.tracker, project)
        self.wait_window(dialog)
        if dialog.result:
            self.load_projects()
    
    def update_status(self, project, new_status):
        """Update a project's status."""
        try:
            self.tracker.update_project_status(project.project_id, new_status)
            self.load_projects()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update status: {str(e)}")
    
    def delete_project(self, project):
        """
        Delete a project with confirmation dialog.
        
        Shows a detailed confirmation dialog with:
        - Project name
        - Warning about yarn associations being removed
        - Warning about irreversibility
        """
        # Get project details for the confirmation message
        project_details = []
        if project.start_date:
            project_details.append(f"Started: {project.start_date}")
        if project.status:
            project_details.append(f"Status: {get_status_display(project.status)}")
        
        details_text = "\n".join(project_details) if project_details else ""
        if details_text:
            details_text = f"\n\n{details_text}"
        
        # Get yarn count for the project
        project_with_yarns = self.tracker.get_project(project.project_id)
        yarn_count = len(project_with_yarns.yarns) if project_with_yarns else 0
        
        yarn_warning = ""
        if yarn_count > 0:
            yarn_warning = f"\n\nThis project uses {yarn_count} yarn{'s' if yarn_count != 1 else ''}.\nThese associations will be removed."
        
        # Show confirmation dialog
        if messagebox.askyesno(
            "Delete Project",
            f"Are you sure you want to delete '{project.project_name}'?{details_text}{yarn_warning}\n\n This action cannot be undone!",
            icon='warning'
        ):
            try:
                # Delete the project using the CRUD method
                if self.tracker.delete_project(project.project_id):
                    messagebox.showinfo(
                        "Success",
                        f"Project '{project.project_name}' deleted successfully!"
                    )
                    # Refresh the project list
                    self.load_projects()
                else:
                    messagebox.showerror(
                        "Error",
                        f"Could not delete '{project.project_name}'. The project may have already been deleted."
                    )
            except Exception as e:
                # Handle specific error cases
                error_msg = str(e)
                if "FOREIGN KEY" in error_msg:
                    messagebox.showerror(
                        "Cannot Delete",
                        f"Cannot delete '{project.project_name}' because it is referenced by other records.\n\n"
                        "This may happen if there are yarn associations that couldn't be removed."
                    )
                else:
                    messagebox.showerror(
                        "Error",
                        f"Failed to delete project: {error_msg}"
                    )
