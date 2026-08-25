"""
============================================================
Styles and Theme Configuration for Knitting Tracker GUI
============================================================
This module defines all visual styling for the application:
- Colour schemes (dark/light mode support)
- Font settings
- Status colours and display names
- Theme configuration

Author: Anna Khoriakova
Last Updated: 2026-08-24
============================================================
"""

import customtkinter as ctk

# Configure default theme
ctk.set_appearance_mode("dark")      # Options: "dark", "light", "system"
ctk.set_default_colour_theme("blue")  # Options: "blue", "green", "dark-blue"

# ============================================================
# COLOUR SCHEMES
# ============================================================

COLOURS = {
    # Primary brand colours
    'primary': '#2B6A9E',
    'primary_light': '#3B8AC4',
    'primary_dark': '#1A4A6E',
    
    # Status colours
    'success': '#2E7D32',
    'warning': '#ED6C02',
    'danger': '#D32F2F',
    'info': '#0288D1',
    
    # Neutral colours (dark mode default)
    'background': '#1A1A1A',
    'surface': '#2D2D2D',
    'surface_light': '#3D3D3D',
    'surface_dark': '#1E1E1E',
    'text': '#FFFFFF',
    'text_secondary': '#AAAAAA',
    'text_disabled': '#666666',
    'border': '#404040',
    'border_light': '#505050',
}

# ============================================================
# FONT SETTINGS
# ============================================================

FONTS = {
    'title': ('Helvetica', 24, 'bold'),
    'heading': ('Helvetica', 18, 'bold'),
    'subheading': ('Helvetica', 14, 'bold'),
    'body': ('Helvetica', 12),
    'body_small': ('Helvetica', 10),
    'body_large': ('Helvetica', 14),
    'button': ('Helvetica', 12, 'bold'),
    'monospace': ('Courier', 11),
}

# ============================================================
# STATUS CONFIGURATIONS
# ============================================================

# Colour mapping for project statuses
STATUS_COLOURS = {
    'Planning': '#ED6C02',      # Orange - planning phase
    'WIP': '#2B6A9E',           # Blue - work in progress
    'Blocking': '#9C27B0',      # Purple - blocking/finishing
    'Finished': '#2E7D32',      # Green - completed
    'Frogged': '#D32F2F',       # Red - frogged/ripped out
    'Abandoned': '#757575',     # Grey - abandoned
}

# Display names 
STATUS_DISPLAY = {
    'Planning': 'Planning',
    'WIP': 'In Progress',
    'Blocking': 'Blocking',
    'Finished': 'Finished',
    'Frogged': 'Frogged',
    'Abandoned': 'Abandoned',
}

# Status ordering for dropdowns
STATUS_ORDER = ['Planning', 'WIP', 'Blocking', 'Finished', 'Frogged', 'Abandoned']
