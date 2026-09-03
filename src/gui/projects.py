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
    