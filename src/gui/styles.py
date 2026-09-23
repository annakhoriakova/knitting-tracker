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
Last Updated: 2026-09-23
============================================================
"""

import customtkinter as ctk

# Configure default theme
ctk.set_appearance_mode("dark")      
ctk.set_default_color_theme("blue")  # CTk's built-in accent theme 
                                      

# ============================================================
# COLOR SCHEMES
# ============================================================
# Each value below is a (light_mode_color, dark_mode_color) tuple.
# Light mode = light pink, dark mode = dark pink.

COLORS = {
    # Primary brand colors
    'primary': ('#8C2F52', '#F5A9C0'),
    'primary_light': ('#A6486B', '#F7BED0'),
    'primary_dark': ('#732541', '#F0839E'),

    # Button colors: light mode = dark pink buttons, dark mode = pastel pink buttons
    'button': ('#8C2F52', '#F5A9C0'),
    'button_hover': ('#732541', '#F0839E'),
    'button_text': ('#FFEAF1', '#4A1F2B'),

    # Status colors
    'success': ('#3F8F5B', '#4CAF6D'),
    'warning': ('#D98A2B', '#E8A23F'),
    'danger': ('#C0395C', '#D9486B'),
    'info': ('#3C8FB0', '#4FA8C9'),

    # Screen/surface colors: light mode = pastel pink screen, dark mode =
    # dark pink screen (opposite of the buttons above for contrast)
    'background': ('#FBE4EC', '#2B0F1C'),
    'surface': ('#FFD9E6', '#3A1526'),
    'surface_light': ('#FFCCE0', '#4A1B30'),
    'surface_dark': ('#F8BFD4', '#210B15'),
    'text': ('#4A1F2B', '#FADCE6'),
    'text_secondary': ('#8C5768', '#D79CB0'),
    'text_disabled': ('#C79AAA', '#7A4A57'),
    'placeholder': ('#E0A9BF', '#A9647D'),
    'border': ('#F3B8CB', '#5C2A38'),
    'border_light': ('#FAD1DE', '#6E3644'),
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
