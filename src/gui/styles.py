"""
============================================================
Styles and Theme Configuration for Knitting Tracker GUI
============================================================
This module defines all visual styling for the application:
- Color schemes (dark/light mode support)
- Font settings
- Status colors and display names
- Theme configuration

Author: Anna Khoriakova
Last Updated: 2026-08-24
============================================================
"""

import customtkinter as ctk

# Configure default theme
ctk.set_appearance_mode("dark")      # Options: "dark", "light", "system"
ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

# ============================================================
# COLOR SCHEMES
# ============================================================

COLORS = {
    # Primary brand colors
    'primary': '#2B6A9E',
    'primary_light': '#3B8AC4',
    'primary_dark': '#1A4A6E',
    
    # Status colors
    'success': '#2E7D32',
    'warning': '#ED6C02',
    'danger': '#D32F2F',
    'info': '#0288D1',
    
    # Neutral colors (dark mode default)
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

# Color mapping for project statuses
STATUS_COLORS = {
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

# ============================================================
# WEIGHT CATEGORIES
# ============================================================

YARN_WEIGHTS = [
    'Lace',
    'Fingering',
    'Sport',
    'DK',
    'Worsted',
    'Aran',
    'Bulky',
    'Super Bulky',
    'Jumbo'
]

# ============================================================
# NEEDLE TYPES
# ============================================================

NEEDLE_TYPES = [
    'Circular',
    'Straight',
    'DPN',              # Double Pointed Needles
    'Interchangeable'
]

NEEDLE_MATERIALS = [
    'Wood',
    'Metal',
    'Bamboo',
    'Plastic',
    'Carbon Fiber'
]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_status_color(status: str) -> str:
    """
    Get the color for a given project status.
    
    Args:
        status: The project status string
    
    Returns:
        str: The hex color code, or grey if status not found
    """
    return STATUS_COLORS.get(status, '#757575')

def get_status_display(status: str) -> str:
    """
    Get the display name for a given project status.
    
    Args:
        status: The project status string
    
    Returns:
        str: The user-friendly display name, or the original if not found
    """
    return STATUS_DISPLAY.get(status, status)

# ============================================================
# NEEDLE LENGTHS
# ============================================================

NEEDLE_LENGTHS = [
    '8', '10', '12', '14', '16', '20', '24', '32', '40', '48', '60'
]

# ============================================================
# YARN WEIGHT CATEGORIES
# ============================================================

YARN_WEIGHTS = [
    'Lace',
    'Fingering',
    'Sport',
    'DK',
    'Worsted',
    'Aran',
    'Bulky',
    'Super Bulky',
    'Jumbo'
]
