"""
============================================================
Unit Tests for the Database Module
============================================================
These tests verify database connections, schema initialization,
and ensure the database operations work correctly.

Author: Anna Khoriakova
Last Updated: 2026-08-22
============================================================
"""

import pytest
import os
import sqlite3
from pathlib import Path
from src.database import Database

class TestDatabase:
    """
    Test suite for the Database class.
    
    Tests cover:
    
    The class uses pytest fixtures for setup and teardown:
    - tmp_path: pytest-provided temporary directory
    - temp_db_path: path to the test database file
    - db: initialized Database instance ready for testing
    """
    
    @pytest.fixture
    def temp_db_path(self, tmp_path):
        """
        Fixture that creates a path for a temporary database.
        
        Args:
            tmp_path: pytest's built-in temporary path fixture
            
        Returns:
            str: Path to the temporary database file
            
        This fixture runs before each test and the tmp_path
        is automatically cleaned up after the test completes.
        """
        db_file = tmp_path / "test_knitting.db"
        return str(db_file)
    
    @pytest.fixture
    def db(self, temp_db_path, tmp_path):
        """
        Fixture that creates a Database instance with a temporary database.
        
        This fixture:
        1. Creates the schema SQL file in the temp directory
        2. Changes to the temp directory so Database can find the schema
        3. Initializes a Database instance
        4. Yields it for testing
        5. Cleans up by changing back to the original directory
        
        This ensures each test gets a fresh, clean database.
        
        Args:
            temp_db_path: Path to temporary database file
            
        Yields:
            Database: Initialized Database instance
            
        The schema is written to a file because Database._initialize_database
        reads the schema from disk (knitting_schema.sql).
        """
        # Create the schema file in the temp directory
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
        
        # Write schema to file in temp directory
        with open(schema_path, "w") as f:
            f.write(schema_content)
        
        # Change to temp directory so Database can find the schema
        original_dir = os.getcwd()
        os.chdir(tmp_path)
        
        # Create Database instance (this will initialize tables)
        db = Database(db_path=temp_db_path)
        
        # Yield for tests to use
        yield db
        
        # Cleanup: return to original directory
        os.chdir(original_dir)
