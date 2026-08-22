"""
============================================================
Unit Tests for the CRUD Operations
============================================================
These tests verify that all database operations work correctly,
including creating, reading, updating, and deleting records.

Author: Anna Khoriakova
Last Updated: 2026-08-22
============================================================
"""

import pytest
from src.crud import KnittingTracker
from src.models import Pattern, Needle, Yarn, Project
from src.database import Database
