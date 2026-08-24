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

    def update_pattern(self, pattern_id: int, pattern: Pattern) -> bool:
        """
        Update an existing pattern in the database.
        
        Args:
            pattern_id: The ID of the pattern to update.
            pattern: Pattern object with updated values.
        
        Returns:
            bool: True if the pattern was found and updated.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE PATTERN 
                SET pattern_name = ?, designer = ?
                WHERE pattern_id = ?
            """, (pattern.pattern_name, pattern.designer, pattern_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_pattern(self, pattern_id: int) -> bool:
        """
        Delete a pattern from the database.
        
        Will fail if the pattern is referenced by any project
        (ON DELETE RESTRICT constraint).
        
        Args:
            pattern_id: The ID of the pattern to delete.
        
        Returns:
            bool: True if the pattern was deleted.
        
        Raises:
            sqlite3.IntegrityError: If pattern is referenced by a project.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM PATTERN WHERE pattern_id = ?", (pattern_id,))
            conn.commit()
            return cursor.rowcount > 0

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

    def update_needle(self, needle_id: int, needle: Needle) -> bool:
        """
        Update an existing needle in the database.
        
        Args:
            needle_id: The ID of the needle to update.
            needle: Needle object with updated values.
        
        Returns:
            bool: True if the needle was found and updated.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE NEEDLE 
                SET needle_size_mm = ?, needle_type = ?, needle_material = ?,
                    needle_length = ?, needle_brand = ?
                WHERE needle_id = ?
            """, (needle.needle_size_mm, needle.needle_type, needle.needle_material,
                    needle.needle_length, needle.needle_brand, needle_id))
            conn.commit()
            return cursor.rowcount > 0

    def delete_needle(self, needle_id: int) -> bool:
        """
        Delete a needle from the database.
        
        Will fail if the needle is referenced by any project
        (ON DELETE RESTRICT constraint).
        
        Args:
            needle_id: The ID of the needle to delete.
        
        Returns:
            bool: True if the needle was deleted.
        
        Raises:
            sqlite3.IntegrityError: If needle is referenced by a project.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM NEEDLE WHERE needle_id = ?", (needle_id,))
            conn.commit()
            return cursor.rowcount > 0

    def get_needle(self, needle_id: int) -> Optional[Needle]:
        """
        Retrieve a needle from the database by its ID.
        
        Args:
            needle_id: The unique identifier of the needle to retrieve.
        
        Returns:
            Optional[Needle]: A Needle object if found, None otherwise.
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM NEEDLE WHERE needle_id = ?", (needle_id,))
            row = cursor.fetchone()
            if row:
                return Needle(**dict(row))
            return None

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

    def create_project(self, project: Project) -> int:
        """
        Create a new project in the database.
        
        This creates the main project record. After creating a project,
        add_yarn_to_project() can be used to associate yarns with it.
        
        Args:
            project: A Project dataclass instance with project details.
                    Requires project_name, pattern_id, and needle_id.
                    Status defaults to 'Planning' if not specified.
                    start_date and end_date should be in ISO format (YYYY-MM-DD).
        
        Returns:
            int: The auto-generated project_id of the newly created project.
        
        Raises:
            sqlite3.IntegrityError: If required fields are NULL or foreign key
                                    constraints are violated (invalid pattern_id/needle_id).
        
        Example:
            project = Project(
                project_name="Aran Sweater",
                start_date="2026-08-21",
                status="Planning",
                recipient="Me",
                pattern_id=1,
                needle_id=3
            )
            project_id = tracker.create_project(project)
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PROJECT (
                    project_name, start_date, end_date, status, 
                    recipient, pattern_id, needle_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                project.project_name, project.start_date, project.end_date, project.status,
                project.recipient, project.pattern_id, project.needle_id
            ))
            project_id = cursor.lastrowid
            conn.commit()
            return project_id
        
    def get_project(self, project_id: int) -> Optional[Project]:
        """
        Retrieve a complete project with all its associated yarns.
        
        This method performs a two-step query:
        1. Gets the main project record
        2. Gets all yarns linked to this project via PROJECT_YARN table
        (including the number of skeins used for each yarn)
        
        The yarns are stored in the Project.yarns attribute as a list of
        dictionaries, each containing yarn details plus skeins_used.
        
        Args:
            project_id: The unique identifier of the project to retrieve.
        
        Returns:
            Optional[Project]: A Project object with populated yarns list,
                            or None if no project exists with the given ID.
        
        Example:
            project = tracker.get_project(1)
            if project:
                print(f"Project: {project.project_name}")
                for yarn_data in project.yarns:
                    print(f"  - {yarn_data['yarn_brand']} x {yarn_data['skeins_used']} skeins")
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            
            # Get the main project information
            cursor.execute("SELECT * FROM PROJECT WHERE project_id = ?", (project_id,))
            row = cursor.fetchone()
            if not row:
                return None
            
            # Convert the row to a Project object
            project = Project(**dict(row))
            
            # Get all yarns associated with this project (both yarn details and the number of skeins used)
            cursor.execute("""
                SELECT y.*, py.skeins_used 
                FROM YARN y
                JOIN PROJECT_YARN py ON y.yarn_id = py.yarn_id
                WHERE py.project_id = ?
            """, (project_id,))
            # Store the yarn data (including skeins_used) in the project's yarns list
            project.yarns = [dict(row) for row in cursor.fetchall()]
            
            return project

    def get_all_projects(self) -> List[Project]:
        """
        Retrieve all projects from the database, sorted by start date (newest first).
        
        This method returns the project details, not the associated yarns.
        get_project() can be used to retrieve the yarn information for a specific project.
        
        Returns:
            List[Project]: A list of all Project objects, with the most recent
                        projects first. Returns empty list if no projects exist.
        
        Example:
            all_projects = tracker.get_all_projects()
            for project in all_projects:
                print(f"{project.project_name} - {project.status}")
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM PROJECT ORDER BY start_date DESC")
            rows = cursor.fetchall()
            return [Project(**dict(row)) for row in rows]
        
    def update_project_status(self, project_id: int, new_status: str) -> bool:
        """
        Update the status of an existing project.
        
        This method also automatically sets the end_date to the current date
        when the status is changed to 'Finished'. This provides automatic
        completion tracking without requiring a separate date update.
        
        Args:
            project_id: The ID of the project to update.
            new_status: The new status to set. Must be one of:
                        'Planning', 'WIP', 'Blocking', 'Finished', 'Frogged', 'Abandoned'
        
        Returns:
            bool: True if the project was found and updated, False if no project
                was found with the given ID.
        
        Raises:
            ValueError: If new_status is not one of the valid status values.
        
        Example:
            # Mark a project as finished
            if tracker.update_project_status(1, 'Finished'):
                print("Project completed!")
            
            # Move a project to blocking (e.g., waiting for more yarn)
            tracker.update_project_status(1, 'Blocking')
        """
        valid_statuses = ['Planning', 'WIP', 'Blocking', 'Finished', 'Frogged', 'Abandoned']
        if new_status not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            # Use a CASE statement to automatically set end_date when finished
            cursor.execute("""
                UPDATE PROJECT 
                SET status = ?, 
                    end_date = CASE WHEN ? = 'Finished' THEN date('now') ELSE end_date END
                WHERE project_id = ?
            """, (new_status, new_status, project_id))
            conn.commit()
            # Return True if any rows were affected (i.e., project was found)
            return cursor.rowcount > 0
        
    def add_yarn_to_project(self, project_id: int, yarn_id: int, skeins_used: int = 1) -> bool:
        """
        Associate a yarn with a project in the PROJECT_YARN junction table.
        
        This allows tracking which yarns are used in a project and how many
        skeins of each are needed/used. A project can have multiple yarns
        (e.g., for stripes, colorwork, or using different yarns for different parts).
        
        Args:
            project_id: The ID of the project to associate the yarn with.
            yarn_id: The ID of the yarn to add to the project.
            skeins_used: Number of skeins of this yarn used in the project.
                        Must be > 0 (validated by database CHECK constraint).
                        Defaults to 1 if not specified.
        
        Returns:
            bool: True if the association was created successfully.
        
        Raises:
            sqlite3.IntegrityError: If the project_id or yarn_id doesn't exist,
                                    or if the combination already exists
                                    (due to composite primary key constraint).
        
        Example:
            # Use 3 skeins of Malabrigo Rios for a sweater
            tracker.add_yarn_to_project(1, 5, 3)
            
            # Use 1 skein of a contrast color for stripes
            tracker.add_yarn_to_project(1, 7, 1)
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO PROJECT_YARN (
                    project_id, yarn_id, skeins_used
                )
                VALUES (?, ?, ?)
            """, (
                project_id, yarn_id, skeins_used
            ))
            conn.commit()
            return True

    # ============ SEARCH & FILTER ============

    def get_active_projects(self) -> List[Project]:
        """
        Retrieve all active projects (Planning, WIP, or Blocking status).
        
        This is a convenience method for quickly viewing projects that are
        currently in progress or planned, excluding finished or abandoned projects.
        Projects are sorted with the most recently started first.
        
        Returns:
            List[Project]: A list of active Project objects, sorted by start_date
                        descending (newest first). Returns empty list if none.
        
        Example:
            active = tracker.get_active_projects()
            print(f"You have {len(active)} active projects:")
            for project in active:
                print(f"  {project.project_name} - {project.status}")
        """
        with self.db.get_connection() as conn:
            cursor = conn.cursor()
            # Filter for projects that are not yet finished, frogged, or abandoned
            cursor.execute("""
                SELECT * FROM PROJECT 
                WHERE status IN ('Planning', 'WIP', 'Blocking')
                ORDER BY start_date DESC
            """)
            rows = cursor.fetchall()
            return [Project(**dict(row)) for row in rows]
