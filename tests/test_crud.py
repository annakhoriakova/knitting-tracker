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

class TestCrudOperations:
    """
    Test suite for KnittingTracker CRUD operations.
    
    Tests are organized by entity (Pattern, Needle, Yarn, Project)
    and then by operation (create, read, update).
    
    Test fixtures:
    - tracker: Creates a fresh KnittingTracker with temp database
    - sample_pattern: Provides a test pattern
    - sample_needle: Provides a test needle
    - sample_yarn: Provides a test yarn
    """
    
    @pytest.fixture
    def tracker(self, tmp_path):
        """
        Fixture that creates a KnittingTracker with a temporary database.
        
        This fixture:
        1. Creates a temporary database file
        2. Creates the schema file in the temp directory
        3. Initializes a KnittingTracker with the temp database
        
        This gives each test a fresh database, ensuring
        tests don't interfere with each other.
        
        Args:
            tmp_path: pytest's temporary directory fixture
            
        Returns:
            KnittingTracker: A tracker instance with temp database
        """
        db_path = str(tmp_path / "test_knitting.db")
        
        # Create schema file in temp directory
        schema_path = tmp_path / "knitting_schema.sql"
        schema_content = """
        CREATE TABLE PATTERN (
            pattern_id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_name TEXT NOT NULL,
            designer TEXT
        );
        CREATE TABLE NEEDLE (
            needle_id INTEGER PRIMARY KEY AUTOINCREMENT,
            needle_size_mm REAL NOT NULL,
            needle_type TEXT NOT NULL,
            needle_material TEXT,
            needle_length TEXT,
            needle_brand TEXT
        );
        CREATE TABLE YARN (
            yarn_id INTEGER PRIMARY KEY AUTOINCREMENT,
            yarn_brand TEXT NOT NULL,
            yarn_line TEXT,
            colour_name TEXT,
            dye_lot TEXT,
            weight_category TEXT,
            total_yardage INTEGER
        );
        CREATE TABLE PROJECT (
            project_id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            start_date TEXT,
            end_date TEXT,
            status TEXT NOT NULL CHECK (status IN ('Planning', 'WIP', 'Blocking', 'Finished', 'Frogged', 'Abandoned')) DEFAULT 'Planning',
            recipient TEXT,
            pattern_id INTEGER NOT NULL,
            needle_id INTEGER NOT NULL,
            FOREIGN KEY (pattern_id) REFERENCES PATTERN(pattern_id) ON DELETE RESTRICT,
            FOREIGN KEY (needle_id) REFERENCES NEEDLE(needle_id) ON DELETE RESTRICT
        );
        CREATE TABLE PROJECT_YARN (
            project_id INTEGER NOT NULL,
            yarn_id INTEGER NOT NULL,
            skeins_used INTEGER DEFAULT 1 CHECK (skeins_used > 0),
            PRIMARY KEY (project_id, yarn_id),
            FOREIGN KEY (project_id) REFERENCES PROJECT(project_id) ON DELETE CASCADE,
            FOREIGN KEY (yarn_id) REFERENCES YARN(yarn_id) ON DELETE RESTRICT
        );
        """
        
        with open(schema_path, "w") as f:
            f.write(schema_content)
        
        # Create tracker with db path
        tracker = KnittingTracker()
        tracker.db = Database(db_path=db_path)
        
        return tracker
    
    @pytest.fixture
    def sample_pattern(self):
        """Create a sample pattern for testing."""
        return Pattern(pattern_name="Test Pattern", designer="Test Designer")
    
    @pytest.fixture
    def sample_needle(self):
        """Create a sample needle for testing."""
        return Needle(
            needle_size_mm=4.0,
            needle_type="Circular",
            needle_material="Metal",
            needle_length="24",
            needle_brand="TestBrand"
        )
    
    @pytest.fixture
    def sample_yarn(self):
        """Create a sample yarn for testing."""
        return Yarn(
            yarn_brand="TestBrand",
            yarn_line="TestLine",
            colour_name="TestColor",
            dye_lot="123",
            weight_category="Worsted",
            total_yardage=200
        )
