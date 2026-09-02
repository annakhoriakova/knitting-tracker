"""
============================================================
Dashboard View
============================================================
The dashboard provides an overview of the knitting tracker:
- Statistics cards (total projects, WIP, finished, patterns)
- Recent projects list
- Quick status overview

Author: Anna Khoriakova
Last Updated: 2026-09-01
============================================================
"""

import customtkinter as ctk
from src.crud import KnittingTracker
from src.gui.styles import COLORS, FONTS, get_status_color, get_status_display

class DashboardView(ctk.CTkFrame):
    """
    Dashboard showing project statistics and recent activity.
    
    This view provides a high-level overview of all knitting projects
    with visual statistics and a list of recent projects.
    """
    
    def __init__(self, parent):
        """Initialize the dashboard view."""
        super().__init__(parent, fg_color="transparent")
        
        self.tracker = KnittingTracker()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Build the dashboard
        self.create_header()
        self.create_stats()
        self.create_recent_projects()
    
    def create_header(self):
        """Create the dashboard header with title and subtitle."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        title = ctk.CTkLabel(
            header_frame,
            text="Dashboard",
            font=FONTS['title']
        )
        title.grid(row=0, column=0, sticky="w")
        
        subtitle = ctk.CTkLabel(
            header_frame,
            text="Welcome back! Here's an overview of your knitting projects.",
            font=FONTS['body'],
            text_color=COLORS['text_secondary']
        )
        subtitle.grid(row=1, column=0, sticky="w")
    
    def create_stats(self):
        """Create statistics cards showing key metrics."""
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        
        # Configure equal column weights for 4 cards
        for i in range(4):
            stats_frame.grid_columnconfigure(i, weight=1)
        
        # Get statistics from database
        stats = self.get_stats()
        
        # Create stat cards
        stat_items = [
            ("Total Projects", stats['total']),
            ("In Progress", stats['wip']),
            ("Finished", stats['finished']),
            ("Patterns", stats['patterns']),
        ]
        
        for i, (label, value) in enumerate(stat_items):
            card = ctk.CTkFrame(stats_frame, corner_radius=15)
            card.grid(row=0, column=i, padx=10, sticky="nsew")
            
            value_label = ctk.CTkLabel(
                card,
                text=str(value),
                font=('Helvetica', 32, 'bold')
            )
            value_label.grid(row=0, column=0, padx=20, pady=(15, 5))
            
            label_label = ctk.CTkLabel(
                card,
                text=label,
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            label_label.grid(row=1, column=0, padx=20, pady=(0, 15))
    
    def get_stats(self):
        """
        Calculate statistics from the database.
        
        Returns:
            dict: Dictionary containing statistics counts
        """
        projects = self.tracker.get_all_projects()
        patterns = self.tracker.get_all_patterns()
        
        stats = {
            'total': len(projects),
            'wip': sum(1 for p in projects if p.status in ['Planning', 'WIP', 'Blocking']),
            'finished': sum(1 for p in projects if p.status == 'Finished'),
            'patterns': len(patterns),
        }
        return stats
    
    def create_recent_projects(self):
        """Create the recent projects list section."""
        # Section title
        title = ctk.CTkLabel(
            self,
            text="Recent Projects",
            font=FONTS['heading']
        )
        title.grid(row=2, column=0, sticky="w", pady=(0, 10))
        
        # Scrollable container for projects
        self.projects_container = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent"
        )
        self.projects_container.grid(row=3, column=0, sticky="nsew")
        self.projects_container.grid_columnconfigure(0, weight=1)
        
        # Load projects
        self.load_recent_projects()
    
    def load_recent_projects(self):
        """Load and display the most recent projects."""
        # Clear existing items
        for widget in self.projects_container.winfo_children():
            widget.destroy()
        
        # Get projects (most recent first)
        projects = self.tracker.get_all_projects()[:5]
        
        if not projects:
            empty_label = ctk.CTkLabel(
                self.projects_container,
                text="No projects yet. Start your first project!",
                font=FONTS['body'],
                text_color=COLORS['text_secondary']
            )
            empty_label.grid(row=0, column=0, pady=20)
            return
        
        for i, project in enumerate(projects):
            self.create_project_item(project, i)
    
    def create_project_item(self, project, index):
        """
        Create a single project item in the list.
        
        Args:
            project: The project object to display
            index: The row index for grid positioning
        """
        item = ctk.CTkFrame(self.projects_container, corner_radius=10)
        item.grid(row=index, column=0, sticky="ew", pady=5)
        item.grid_columnconfigure(0, weight=1)
        
        # Project name
        name_label = ctk.CTkLabel(
            item,
            text=project.project_name,
            font=FONTS['subheading']
        )
        name_label.grid(row=0, column=0, padx=15, pady=(10, 0), sticky="w")
        
        # Status with color
        status_display = get_status_display(project.status)
        status_color = get_status_color(project.status)
        
        status_label = ctk.CTkLabel(
            item,
            text=status_display,
            font=FONTS['body'],
            text_color=status_color
        )
        status_label.grid(row=1, column=0, padx=15, pady=(0, 10), sticky="w")
        
        # Details (start date, recipient, etc.)
        details = []
        if project.start_date:
            details.append(f"Started: {project.start_date}")
        if project.recipient:
            details.append(f"{project.recipient}")
        
        details_text = " | ".join(details)
        if details_text:
            details_label = ctk.CTkLabel(
                item,
                text=details_text,
                font=FONTS['body_small'],
                text_color=COLORS['text_secondary']
            )
            details_label.grid(row=2, column=0, padx=15, pady=(0, 10), sticky="w")
            