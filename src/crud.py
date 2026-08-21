"""
============================================================
CRUD Operations Module for Knitting Tracker Application
============================================================
This module provides the main data access layer for the knitting tracker,
implementing Create, Read, Update, and Delete operations for all database entities.

The KnittingTracker class includes all database operations, handling:
- Database connections via context managers (ensuring proper cleanup)
- Data conversion between Python dataclasses and database rows
- Queries involving multiple tables (e.g., projects with their yarns)
- Data validation before database operations

Dependencies:
    - Database class from src.database for connection management
    - Dataclass models from src.models for data representation

Author: Anna Khoriakova
Last Updated: 2026-08-21
============================================================
"""

from typing import List, Optional
from src.database import Database
from src.models import Pattern, Needle, Yarn, Project
