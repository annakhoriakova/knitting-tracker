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
    - Database initialization and schema creation
    - Connection management with context manager
    - Multiple connections and resource cleanup
    - Error handling and edge cases
    
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
            color_name TEXT,
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

    def test_database_initialization(self, db, temp_db_path):
            """
            Test that the database initializes correctly.
            
            Verifies that:
            - The database file is created on disk
            - The db_path attribute matches the expected path
            - The database is ready for connections
            """
            # Assert the database file was created
            assert os.path.exists(temp_db_path)
            # Assert the path was stored correctly
            assert db.db_path == temp_db_path
        
    def test_tables_created(self, db):
        """
        Test that all expected tables are created.
        
        Verifies that:
        - All 5 tables (PATTERN, NEEDLE, YARN, PROJECT, PROJECT_YARN) exist
        - The schema was correctly applied
        - No tables are missing
        
        This test ensures that _initialize_database() correctly
        executed the schema SQL and created all tables.
        """
        with db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Query all table names from SQLite's master table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = [row[0] for row in cursor.fetchall()]
            
            # Define the expected tables (matches schema)
            expected_tables = ['PATTERN', 'NEEDLE', 'YARN', 'PROJECT', 'PROJECT_YARN']
            
            # Check that each expected table exists
            for table in expected_tables:
                assert table in tables, f"Table {table} was not created"

    def test_connection_context_manager(self, db):
        """
        Test that the connection context manager works properly.
        
        Verifies that:
        - get_connection() returns a valid SQLite connection
        - The connection can execute queries
        - The context manager handles cleanup properly
        """
        # Use the context manager
        with db.get_connection() as conn:
            # Assert connection is a SQLite connection object
            assert isinstance(conn, sqlite3.Connection)
            
            # Execute a simple query to verify connection works
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()[0]
            assert result == 1

    def test_connection_closes_properly(self, db):
        """
        Test that connections are closed after context manager exits.
        
        Verifies that:
        - Connection is open while inside the context manager
        - Connection is automatically closed when exiting the context
        - No resources are leaked
        """
        conn = None
        with db.get_connection() as c:
            conn = c
            # Try a simple query to verify connection is active
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()[0]
            assert result == 1
        
        # Trying to execute should raise an error
        # because the connection should be closed
        with pytest.raises(sqlite3.ProgrammingError) as excinfo:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
        
        # Verify the error is about closed connection
        assert "cannot operate on a closed database" in str(excinfo.value).lower()

    def test_multiple_connections(self, db):
        """
        Test that multiple connections can be used simultaneously.
        
        Verifies that:
        - Different connections are unique objects
        - Each connection can be used independently
        - Connections close when their context ends
        """
        # Use two nested context managers
        with db.get_connection() as conn1:
            # Check conn1 is open by executing a query
            cursor1 = conn1.cursor()
            cursor1.execute("SELECT 1")
            assert cursor1.fetchone()[0] == 1
            
            with db.get_connection() as conn2:
                # Assert connections are different objects
                assert conn1 is not conn2
                
                # Both connections should be open and usable
                cursor1 = conn1.cursor()
                cursor1.execute("SELECT 2")
                assert cursor1.fetchone()[0] == 2
                
                cursor2 = conn2.cursor()
                cursor2.execute("SELECT 3")
                assert cursor2.fetchone()[0] == 3
            
            # Trying to use conn2 should raise an error
            with pytest.raises(sqlite3.ProgrammingError) as excinfo:
                cursor = conn2.cursor()
                cursor.execute("SELECT 1")
            assert "cannot operate on a closed database" in str(excinfo.value).lower()
            
            # conn1 should still be open
            cursor1 = conn1.cursor()
            cursor1.execute("SELECT 4")
            assert cursor1.fetchone()[0] == 4
        
        # conn1 should also be closed
        with pytest.raises(sqlite3.ProgrammingError) as excinfo:
            cursor = conn1.cursor()
            cursor.execute("SELECT 1")
        assert "cannot operate on a closed database" in str(excinfo.value).lower()
