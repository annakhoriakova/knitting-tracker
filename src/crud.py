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

class KnittingTracker:
    """
    Main service class for all knitting tracker database operations.
    
    This class provides an interface for interacting with
    the knitting tracker database. Each method corresponds to a specific
    business operation, handling the SQL queries and data mapping.
    
    The class is organized into sections:
    - Pattern operations: Create, read, and list patterns
    - Needle operations: Create and list needles
    - Yarn operations: Create and list yarns
    - Project operations: Create, read, update, and list projects
    - Search & Filter: Specialized queries for common use cases
    
    All methods use the Database class's context manager for connections,
    ensuring proper resource cleanup even if exceptions occur.
    
    Example:
        tracker = KnittingTracker()
        pattern = Pattern(pattern_name="Aran Sweater", designer="Alice Starmore")
        pattern_id = tracker.create_pattern(pattern)
    """
    
    def __init__(self):
        """
        Initialize the KnittingTracker with a database connection.
        
        Creates a Database instance that manages the SQLite connection.
        The database file location is determined by the Database class
        (defaults to "data/knitting.db").
        """
        self.db = Database()

# ============ PATTERN OPERATIONS ============

def create_pattern(self, pattern: Pattern) -> int:
    """
    Insert a new pattern into the database.
    
    Args:
        pattern: A Pattern dataclass instance with pattern details.
                 Must have pattern_name set; designer is optional.
    
    Returns:
        int: The auto-generated pattern_id of the newly created pattern.
    
    Raises:
        sqlite3.IntegrityError: If pattern_name is NULL or violates constraints.
    
    Example:
        pattern = Pattern(pattern_name="Lace Shawl", designer="Jane Doe")
        pattern_id = tracker.create_pattern(pattern)
    """
    with self.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO PATTERN (pattern_name, designer)
            VALUES (?, ?)
        """, (pattern.pattern_name, pattern.designer))
        conn.commit()
        return cursor.lastrowid

def get_pattern(self, pattern_id: int) -> Optional[Pattern]:
    """
    Retrieve a pattern from the database by its ID.
    
    Args:
        pattern_id: The unique identifier of the pattern to retrieve.
    
    Returns:
        Optional[Pattern]: A Pattern object if found, None if no pattern
                           exists with the given ID.
    
    Example:
        pattern = tracker.get_pattern(1)
        if pattern:
            print(f"Found pattern: {pattern.pattern_name}")
    """
    with self.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PATTERN WHERE pattern_id = ?", (pattern_id,))
        row = cursor.fetchone()
        if row:
            # Convert the database row (sqlite3.Row) to a Pattern dataclass
            # dict(row) converts the Row object to a dictionary mapping column names to values
            return Pattern(**dict(row))
        return None

def get_all_patterns(self) -> List[Pattern]:
    """
    Retrieve all patterns from the database, sorted alphabetically by name.
    
    Returns:
        List[Pattern]: A list of all Pattern objects in the database.
                       Returns an empty list if no patterns exist.
    
    Example:
        all_patterns = tracker.get_all_patterns()
        for pattern in all_patterns:
            print(f"{pattern.pattern_name} by {pattern.designer}")
    """
    with self.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM PATTERN ORDER BY pattern_name")
        rows = cursor.fetchall()
        return [Pattern(**dict(row)) for row in rows]

# ============ NEEDLE OPERATIONS ============



# ============ YARN OPERATIONS ============



# ============ PROJECT OPERATIONS ============



# ============ SEARCH & FILTER ============
