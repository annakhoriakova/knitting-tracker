#!/usr/bin/env python3
"""
============================================================
Knitting Tracker Application
============================================================
A desktop application for tracking knitting projects,
patterns, yarns, and needles.

Usage:
    python main.py

Author: Anna Khoriakova
Last Updated: 2026-09-02
============================================================
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.gui.main_window import run_app

if __name__ == "__main__":
    print("Starting Knitting Tracker...")
    print("=" * 40)
    run_app()
