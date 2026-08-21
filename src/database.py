'''
Name: Anna Khoriakova
Date: 2026-08-21
Description: Database layer for the Knitting Project Tracker application.
             Manages SQLite connections and initializes the database schema.
'''

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
    def _initialize_database(self):
        """Create tables if they don't exist
        
        This method reads the SQL schema from a file and executes it
        to set up the database structure on first run.
        """
        