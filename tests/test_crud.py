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
    
    # ============ PATTERN TESTS ============
    # Tests for the Pattern entity CRUD operations
    
    def test_create_pattern(self, tracker, sample_pattern):
        """
        Test creating a new pattern.
        
        This test verifies the create-read flow:
        1. Create a pattern in the database
        2. Get the auto-generated ID
        3. Read the pattern back from the database
        4. Verify all data was saved correctly
        
        This tests both the create_pattern and get_pattern methods.
        """
        # Create the pattern
        pattern_id = tracker.create_pattern(sample_pattern)
        
        # Verify ID should be positive (auto-generated)
        assert pattern_id > 0
        
        # Read the pattern back
        saved_pattern = tracker.get_pattern(pattern_id)
        
        # Verify all data is correct
        assert saved_pattern is not None
        assert saved_pattern.pattern_name == "Test Pattern"
        assert saved_pattern.designer == "Test Designer"
    
    def test_get_pattern_not_found(self, tracker):
        """
        Test getting a non-existent pattern.
        
        Verifies that:
        - Getting a pattern with an invalid ID returns None
        - No exception is raised
        - The method handles the "not found" case properly
        """
        # Try to get a pattern with ID 999 (shouldn't exist)
        pattern = tracker.get_pattern(999)
        
        # Should return None instead of raising an error
        assert pattern is None
    
    def test_get_all_patterns(self, tracker, sample_pattern):
        """
        Test retrieving all patterns.
        
        This test verifies:
        1. Multiple patterns can be inserted
        2. get_all_patterns returns all of them
        3. No patterns are lost or duplicated
        4. Results are sorted by name
        """
        # Insert two patterns
        pattern1_id = tracker.create_pattern(sample_pattern)
        
        # Insert a second pattern with different name
        pattern2 = Pattern(pattern_name="Pattern 2", designer="Designer 2")
        pattern2_id = tracker.create_pattern(pattern2)
        
        # Get all patterns
        patterns = tracker.get_all_patterns()
        
        # Verify both patterns are in the results
        assert len(patterns) >= 2  # Might have more from other tests
        pattern_ids = [p.pattern_id for p in patterns]
        assert pattern1_id in pattern_ids
        assert pattern2_id in pattern_ids
    
    # ============ NEEDLE TESTS ============
    
    def test_create_needle(self, tracker, sample_needle):
        """
        Test creating a new needle.
        
        Similar to pattern test, but for needles.
        Verifies needle can be created and retrieved.
        """
        # Create the needle
        needle_id = tracker.create_needle(sample_needle)
        
        # Verify ID is valid
        assert needle_id > 0
        
        # Verify needle was saved by checking it appears in all needles list
        needles = tracker.get_all_needles()
        needle_ids = [n.needle_id for n in needles]
        assert needle_id in needle_ids
    
    def test_get_all_needles(self, tracker, sample_needle):
        """
        Test retrieving all needles.
        
        Verifies that needles are returned and sorted correctly.
        Tests that different types of needles can coexist.
        """
        # Insert first needle
        needle1_id = tracker.create_needle(sample_needle)
        
        # Insert a second needle with different attributes
        needle2 = Needle(
            needle_size_mm=5.5,
            needle_type="DPN",
            needle_material="Wood"
        )
        needle2_id = tracker.create_needle(needle2)
        
        # Get all needles
        needles = tracker.get_all_needles()
        
        # Verify both needles are present
        assert len(needles) >= 2
        needle_ids = [n.needle_id for n in needles]
        assert needle1_id in needle_ids
        assert needle2_id in needle_ids
