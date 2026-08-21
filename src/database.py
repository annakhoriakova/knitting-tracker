"""
============================================================
Database Layer for Knitting Project Tracker
============================================================
This module handles all database operations including:
- SQLite connection management
- Database initialization and schema setup
- Connection context management for safe resource handling

The database layer works with the models defined in models.py
and the CRUD operations in crud.py.

Author: Anna Khoriakova
Date: 2026-08-21
============================================================
"""

import sqlite3
from contextlib import contextmanager
from typing import List, Dict, Any, Optional
from datetime import datetime

class Database:
    """Handles database connections and basic operations"""
    
    def __init__(self, db_path: str = "data/knitting.db"):
        """Initialize the Database object with a path to the database file
        Args:
            db_path: Path to the SQLite database file (default: "data/knitting.db")
        """
        # Store the database file path as an instance variable
        self.db_path = db_path
        # Call the internal method to create tables if they don't exist
        self._initialize_database()

    @contextmanager
    def get_connection(self):
        """Context manager for database connections
        
        This allows using 'with Database().get_connection() as conn:' syntax
        which automatically handles opening and closing the connection.
        
        Yields:
            sqlite3.Connection: An active database connection
        """
        # Establish a connection to the SQLite database at the stored path
        conn = sqlite3.connect(self.db_path)
        # Set row_factory to sqlite3.Row so query results can be accessed by column name
        conn.row_factory = sqlite3.Row
        try:
            # Yield the connection to the calling code
            yield conn
        finally:
            # Close the database connection to free up resources
            conn.close()
                
    def _initialize_database(self):
        """Create tables if they don't exist
        
        This method reads the SQL schema from a file and executes it
        to set up the database structure on first run.
        """
        # Use the context manager to get a database connection
        with self.get_connection() as conn:
            # Create a cursor object to execute SQL commands
            cursor = conn.cursor()
            
            # Open the schema file in read mode ('r')
            # "knitting_schema.sql" contains all CREATE TABLE statements
            with open("knitting_schema.sql", "r") as f:
                # Read the entire contents of the schema file as a string
                schema = f.read()
            
            # Execute the entire SQL schema as a script
            # This runs all the CREATE TABLE, DROP TABLE, and CREATE INDEX statements
            # The schema file includes DROP statements to clean up existing tables
            # and CREATE statements to build the database structure fresh
            cursor.executescript(schema)
            
            # Commit (save) the changes to the database permanently
            # This makes the table creation permanent
            conn.commit()
