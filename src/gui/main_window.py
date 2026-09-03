"""
============================================================
Main Application Window
============================================================
The main window of the knitting tracker application with:
- Sidebar navigation
- Content area for different views
- Theme toggle
- Application lifecycle management

Author: Anna Khoriakova
Last Updated: 2026-09-02
============================================================
"""

import customtkinter as ctk
from src.gui.styles import COLORS, FONTS
from src.gui.dashboard import DashboardView
from src.gui.projects import ProjectsView
from src.gui.patterns import PatternsView
from src.gui.yarns import YarnsView
from src.gui.needles import NeedlesView


class MainWindow(ctk.CTk):
    """
    Main application window with navigation sidebar.
    
    This is the root window of the application. It manages:
    - Navigation between different views
    - Theme switching (dark/light mode)
    - Application state
    
    Attributes:
        current_view: The currently displayed view (subclass of CTkFrame)
        sidebar: The navigation sidebar
        content_frame: The main content area
    """
    
    def __init__(self):
        """Initialize the main application window."""
        super().__init__()
        
        # Window configuration
        self.title("Knitting Tracker")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        # Configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create UI components
        self.create_sidebar()
        self.create_content_area()
        
        # Show initial view (Dashboard)
        self.current_view = None
        self.show_dashboard()
    
    def create_sidebar(self):
        """
        Create the navigation sidebar.
        
        The sidebar contains:
        - Application title/logo
        - Navigation buttons for each view
        - Theme toggle switch
        - Version information
        """
        # Sidebar frame with dark background
        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(8, weight=1)  # Push footer to bottom
        
        # App title
        title_label = ctk.CTkLabel(
            self.sidebar,
            text="Knitting\nTracker",
            font=('Helvetica', 20, 'bold'),
            justify="center"
        )
        title_label.grid(row=0, column=0, padx=20, pady=(30, 20))
        
        # Navigation buttons
        nav_items = [
            ("Dashboard", self.show_dashboard),
            ("Projects", self.show_projects),
            ("Patterns", self.show_patterns),
            ("Yarns", self.show_yarns),
            ("Needles", self.show_needles),
        ]
        
        # Store button references for styling
        self.nav_buttons = []
        
        for i, (text, command) in enumerate(nav_items, start=1):
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                corner_radius=10,
                height=40,
                font=FONTS['body']
            )
            btn.grid(row=i, column=0, padx=20, pady=5, sticky="ew")
            self.nav_buttons.append(btn)
        
        # Theme toggle at bottom
        self.theme_toggle = ctk.CTkSwitch(
            self.sidebar,
            text="Dark Mode",
            command=self.toggle_theme,
            font=FONTS['body_small']
        )
        self.theme_toggle.grid(row=9, column=0, padx=20, pady=20, sticky="s")
        self.theme_toggle.select()  # Dark mode by default
        
        # Version info
        version_label = ctk.CTkLabel(
            self.sidebar,
            text="v0.1.0",
            font=FONTS['body_small'],
            text_color=COLORS['text_secondary']
        )
        version_label.grid(row=10, column=0, padx=20, pady=(0, 10))
    
    def create_content_area(self):
        """
        Create the main content area where views are displayed.
        """
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def clear_content(self):
        """
        Clear the content area by destroying the current view.
        """
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
    
    def show_dashboard(self):
        """Show the dashboard view."""
        self.clear_content()
        self.current_view = DashboardView(self.content_frame)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def show_projects(self):
        """Show the projects management view."""
        self.clear_content()
        self.current_view = ProjectsView(self.content_frame)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def show_patterns(self):
        """Show the patterns management view."""
        self.clear_content()
        self.current_view = PatternsView(self.content_frame)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def show_yarns(self):
        """Show the yarns management view."""
        self.clear_content()
        self.current_view = YarnsView(self.content_frame)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def show_needles(self):
        """Show the needles management view."""
        self.clear_content()
        self.current_view = NeedlesView(self.content_frame)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def toggle_theme(self):
        """
        Toggle between dark and light mode.
        """
        if self.theme_toggle.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

def run_app():
    """
    Run the main application.
    
    This is the entry point for the GUI application.
    """
    app = MainWindow()
    app.mainloop()
