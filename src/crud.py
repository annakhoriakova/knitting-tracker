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
            INSERT INTO PATTERN (
                pattern_name, designer
            )
            VALUES (?, ?)
        """, (
            pattern.pattern_name, pattern.designer
        ))
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

def create_needle(self, needle: Needle) -> int:
    """
    Insert a new needle into the database.
    
    Args:
        needle: A Needle dataclass instance with needle details.
                Requires needle_size_mm and needle_type.
                Other fields (material, length, brand) are optional.
    
    Returns:
        int: The auto-generated needle_id of the newly created needle.
    
    Raises:
        sqlite3.IntegrityError: If required fields are NULL or constraints are violated.
    
    Example:
        needle = Needle(
            needle_size_mm=4.0,
            needle_type="Circular",
            needle_material="Metal",
            needle_length="24",
            needle_brand="KnitPro"
        )
        needle_id = tracker.create_needle(needle)
    """
    with self.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO NEEDLE (
                needle_size_mm, needle_type, needle_material, 
                needle_length, needle_brand
            )
            VALUES (?, ?, ?, ?, ?)
        """, (
            needle.needle_size_mm, needle.needle_type, needle.needle_material,
            needle.needle_length, needle.needle_brand
        ))
        conn.commit()
        return cursor.lastrowid
    
def get_all_needles(self) -> List[Needle]:
    """
    Retrieve all needles from the database, sorted by size.
    
    Returns:
        List[Needle]: A list of all Needle objects, ordered by needle_size_mm
                      (smallest to largest). Returns empty list if none exist.
    
    Example:
        needles = tracker.get_all_needles()
        for needle in needles:
            print(f"Size {needle.needle_size_mm}mm - {needle.needle_type}")
    """
    with self.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM NEEDLE ORDER BY needle_size_mm")
        rows = cursor.fetchall()
        return [Needle(**dict(row)) for row in rows]

# ============ YARN OPERATIONS ============

def create_yarn(self, yarn: Yarn) -> int:
    """
    Insert a new yarn into the database.
    
    Args:
        yarn: A Yarn dataclass instance with yarn details.
              Requires yarn_brand. All other fields are optional.
    
    Returns:
        int: The auto-generated yarn_id of the newly created yarn.
    
    Raises:
        sqlite3.IntegrityError: If yarn_brand is NULL or constraints are violated.
    
    Example:
        yarn = Yarn(
            yarn_brand="Malabrigo",
            yarn_line="Rios",
            colour_name="Whale's Road",
            weight_category="Worsted",
            total_yardage=210
        )
        yarn_id = tracker.create_yarn(yarn)
    """
    with self.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO YARN (
                yarn_brand, yarn_line, colour_name, dye_lot, 
                weight_category, total_yardage
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            yarn.yarn_brand, yarn.yarn_line, yarn.colour_name, yarn.dye_lot,
            yarn.weight_category, yarn.total_yardage
        ))
        conn.commit()
        return cursor.lastrowid
    
def get_all_yarns(self) -> List[Yarn]:
    """
    Retrieve all yarns from the database, sorted by brand then line.
    
    Returns:
        List[Yarn]: A list of all Yarn objects, ordered alphabetically
                    by brand name, then by line name. Returns empty list if none.
    
    Example:
        yarns = tracker.get_all_yarns()
        for yarn in yarns:
            print(f"{yarn.yarn_brand} {yarn.yarn_line} - {yarn.colour_name}")
    """
    with self.db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM YARN ORDER BY yarn_brand, yarn_line")
        rows = cursor.fetchall()
        return [Yarn(**dict(row)) for row in rows]

# ============ PROJECT OPERATIONS ============



# ============ SEARCH & FILTER ============
