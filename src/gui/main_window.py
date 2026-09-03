"""
============================================================
Main Application Window
============================================================
The main window of the knitting tracker application with:


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
    