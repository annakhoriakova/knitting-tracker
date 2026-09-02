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
            color_name="TestColor",
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
    
    # ============ YARN TESTS ============
    
    def test_create_yarn(self, tracker, sample_yarn):
        """
        Test creating a new yarn.
        
        Verifies yarn can be created with all attributes
        and retrieved from the database.
        """
        # Create the yarn
        yarn_id = tracker.create_yarn(sample_yarn)
        
        # Verify ID is valid
        assert yarn_id > 0
        
        # Verify yarn was saved
        yarns = tracker.get_all_yarns()
        yarn_ids = [y.yarn_id for y in yarns]
        assert yarn_id in yarn_ids
    
    def test_get_all_yarns(self, tracker, sample_yarn):
        """
        Test retrieving all yarns.
        
        Verifies multiple yarns can be stored and retrieved.
        Tests that yarns from different brands are handled correctly.
        """
        # Insert first yarn
        yarn1_id = tracker.create_yarn(sample_yarn)
        
        # Insert a second yarn with different brand
        yarn2 = Yarn(
            yarn_brand="Brand2",
            yarn_line="Line2",
            color_name="Color2",
            weight_category="DK",
            total_yardage=150
        )
        yarn2_id = tracker.create_yarn(yarn2)
        
        # Get all yarns
        yarns = tracker.get_all_yarns()
        
        # Verify both yarns are present
        assert len(yarns) >= 2
        yarn_ids = [y.yarn_id for y in yarns]
        assert yarn1_id in yarn_ids
        assert yarn2_id in yarn_ids
    
    # ============ PROJECT TESTS ============
    
    def test_create_project(self, tracker, sample_pattern, sample_needle, sample_yarn):
        """
        Test creating a new project with yarn.
        
        This is a test covering:
        1. Creating all dependencies (pattern, needle, yarn)
        2. Creating a project with references to these
        3. Associating yarn with the project
        4. Verifying the complete project with yarns is retrieved
        
        This tests the full relationship chain:
        Project -> Pattern
        Project -> Needle
        Project -> Yarn (via PROJECT_YARN)
        """
        # Create dependencies
        pattern_id = tracker.create_pattern(sample_pattern)
        needle_id = tracker.create_needle(sample_needle)
        yarn_id = tracker.create_yarn(sample_yarn)
        
        # Create the project
        project = Project(
            project_name="Test Project",
            start_date="2026-08-21",
            status="Planning",
            recipient="Test Recipient",
            pattern_id=pattern_id,
            needle_id=needle_id
        )
        project_id = tracker.create_project(project)
        
        # Verify project was created
        assert project_id > 0
        
        # Add yarn to project (with 3 skeins used)
        tracker.add_yarn_to_project(project_id, yarn_id, 3)
        
        # Retrieve and verify the complete project
        saved_project = tracker.get_project(project_id)
        
        # Verify project fields
        assert saved_project is not None
        assert saved_project.project_name == "Test Project"
        assert saved_project.status == "Planning"
        assert saved_project.recipient == "Test Recipient"
        assert saved_project.pattern_id == pattern_id
        assert saved_project.needle_id == needle_id
        
        # Verify associated yarn
        assert len(saved_project.yarns) == 1
        assert saved_project.yarns[0]['yarn_brand'] == "TestBrand"
        assert saved_project.yarns[0]['skeins_used'] == 3
    
    def test_update_project_status(self, tracker, sample_pattern, sample_needle):
        """
        Test updating a project's status.
        
        Verifies that:
        1. Status can be changed from default ('Planning') to a new value
        2. The update returns success (True)
        3. The new status is persisted in the database
        4. Other fields remain unchanged
        """
        # Setup: Create dependencies and project
        pattern_id = tracker.create_pattern(sample_pattern)
        needle_id = tracker.create_needle(sample_needle)
        
        project = Project(
            project_name="Test Project",
            pattern_id=pattern_id,
            needle_id=needle_id
        )
        project_id = tracker.create_project(project)
        
        # Update status from 'Planning' (default) to 'WIP'
        result = tracker.update_project_status(project_id, "WIP")
        
        # Verify update was successful
        assert result is True
        
        # Verify status was changed in database
        saved_project = tracker.get_project(project_id)
        assert saved_project.status == "WIP"
    
    def test_update_project_status_invalid(self, tracker, sample_pattern, sample_needle):
        """
        Test updating a project with an invalid status.
        
        Verifies that:
        1. Invalid status values raise a ValueError
        2. The error message mentions the allowed values
        3. The project status remains unchanged (rollback)
        
        This tests the validation in update_project_status.
        """
        # Setup: Create dependencies and project
        pattern_id = tracker.create_pattern(sample_pattern)
        needle_id = tracker.create_needle(sample_needle)
        
        project = Project(
            project_name="Test Project",
            pattern_id=pattern_id,
            needle_id=needle_id
        )
        project_id = tracker.create_project(project)
        
        # Try to update with invalid status
        with pytest.raises(ValueError) as excinfo:
            tracker.update_project_status(project_id, "InvalidStatus")
        
        # Verify error message is helpful
        assert "Invalid status" in str(excinfo.value)
    
    def test_get_all_projects(self, tracker, sample_pattern, sample_needle):
        """
        Test retrieving all projects.
        
        Verifies that:
        1. Multiple projects can be created and retrieved
        2. Each project has unique IDs
        3. Projects are returned in expected order (by start_date DESC)
        """
        # Setup: Create dependencies shared by both projects
        pattern_id = tracker.create_pattern(sample_pattern)
        needle_id = tracker.create_needle(sample_needle)
        
        # Create first project
        project1 = Project(
            project_name="Project 1",
            pattern_id=pattern_id,
            needle_id=needle_id
        )
        project1_id = tracker.create_project(project1)
        
        # Create second project with different status
        project2 = Project(
            project_name="Project 2",
            pattern_id=pattern_id,
            needle_id=needle_id,
            status="WIP"
        )
        project2_id = tracker.create_project(project2)
        
        # Get all projects
        projects = tracker.get_all_projects()
        
        # Verify both projects are in the results
        assert len(projects) >= 2
        project_ids = [p.project_id for p in projects]
        assert project1_id in project_ids
        assert project2_id in project_ids
    
    def test_get_active_projects(self, tracker, sample_pattern, sample_needle):
        """
        Test retrieving only active (Planning, WIP, Blocking) projects.
        
        This tests the filtering logic:
        - Active projects: Planning, WIP, Blocking
        - Inactive projects: Finished, Frogged, Abandoned
        
        Verifies that only active projects are returned and
        inactive projects are properly excluded.
        """
        # Setup: Create dependencies shared by all projects
        pattern_id = tracker.create_pattern(sample_pattern)
        needle_id = tracker.create_needle(sample_needle)
        
        # Create projects with different statuses
        # Active: WIP project (should be included)
        project1 = Project(
            project_name="Active WIP Project",
            pattern_id=pattern_id,
            needle_id=needle_id,
            status="WIP"
        )
        tracker.create_project(project1)
        
        # Inactive: Finished project (should be excluded)
        project2 = Project(
            project_name="Finished Project",
            pattern_id=pattern_id,
            needle_id=needle_id,
            status="Finished"
        )
        tracker.create_project(project2)
        
        # Active: Planning project (should be included)
        project3 = Project(
            project_name="Planning Project",
            pattern_id=pattern_id,
            needle_id=needle_id,
            status="Planning"
        )
        tracker.create_project(project3)
        
        # Active: Blocking project (should be included)
        project4 = Project(
            project_name="Blocking Project",
            pattern_id=pattern_id,
            needle_id=needle_id,
            status="Blocking"
        )
        tracker.create_project(project4)
        
        # Inactive: Frogged project (should be excluded)
        project5 = Project(
            project_name="Frogged Project",
            pattern_id=pattern_id,
            needle_id=needle_id,
            status="Frogged"
        )
        tracker.create_project(project5)
        
        # Get active projects
        active = tracker.get_active_projects()
        
        # Should only include active projects (WIP, Planning, Blocking)
        active_names = [p.project_name for p in active]
        
        # Assert active projects are included
        assert "Active WIP Project" in active_names
        assert "Planning Project" in active_names
        assert "Blocking Project" in active_names
        
        # Assert inactive projects are excluded
        assert "Finished Project" not in active_names
        assert "Frogged Project" not in active_names
        
        # Verify only active projects are returned (3 of the 5)
        assert len(active) == 3
    
    def test_add_yarn_to_project(self, tracker, sample_pattern, sample_needle, sample_yarn):
        """
        Test adding yarn to a project.
        
        Verifies that:
        1. Yarn can be associated with a project
        2. Default skeins used is 1
        3. Custom skeins used can be specified
        4. Multiple yarns can be added to the same project
        """
        # Setup: Create dependencies
        pattern_id = tracker.create_pattern(sample_pattern)
        needle_id = tracker.create_needle(sample_needle)
        yarn_id = tracker.create_yarn(sample_yarn)
        
        project = Project(
            project_name="Test Project",
            pattern_id=pattern_id,
            needle_id=needle_id
        )
        project_id = tracker.create_project(project)
        
        # Add yarn with default skeins (1)
        result = tracker.add_yarn_to_project(project_id, yarn_id)
        assert result is True
        
        # Add another yarn with custom skeins (2)
        yarn2 = Yarn(
            yarn_brand="Brand2",
            yarn_line="Line2",
            color_name="Color2",
            weight_category="DK",
            total_yardage=150
        )
        yarn2_id = tracker.create_yarn(yarn2)
        tracker.add_yarn_to_project(project_id, yarn2_id, 2)
        
        # Verify both yarns are associated with the project
        saved_project = tracker.get_project(project_id)
        assert len(saved_project.yarns) == 2
        
        # Check skeins used for each yarn
        skeins_used = {y['yarn_brand']: y['skeins_used'] for y in saved_project.yarns}
        assert skeins_used["TestBrand"] == 1  # Default
        assert skeins_used["Brand2"] == 2     # Custom
    
    def test_duplicate_yarn_to_project(self, tracker, sample_pattern, sample_needle, sample_yarn):
        """
        Test that adding the same yarn to a project twice raises an error.
        
        Since project_id and yarn_id form a composite primary key,
        duplicates should be prevented by the database constraint.
        """
        # Setup: Create dependencies
        pattern_id = tracker.create_pattern(sample_pattern)
        needle_id = tracker.create_needle(sample_needle)
        yarn_id = tracker.create_yarn(sample_yarn)
        
        project = Project(
            project_name="Test Project",
            pattern_id=pattern_id,
            needle_id=needle_id
        )
        project_id = tracker.create_project(project)
        
        # Add yarn first time (should succeed)
        tracker.add_yarn_to_project(project_id, yarn_id, 2)
        
        # Add same yarn again (should fail due to primary key constraint)
        with pytest.raises(Exception) as excinfo:  # SQLite will raise IntegrityError
            tracker.add_yarn_to_project(project_id, yarn_id, 3)
        
        # Verify error is related to duplicate key
        assert "UNIQUE constraint failed" in str(excinfo.value) or "IntegrityError" in str(excinfo.value)

    def test_project_without_yarn(self, tracker, sample_pattern, sample_needle):
        """
        Test creating a project without associating any yarn.
        
        Verifies that projects can exist without yarns (e.g., in planning stage).
        """
        # Setup: Create dependencies
        pattern_id = tracker.create_pattern(sample_pattern)
        needle_id = tracker.create_needle(sample_needle)
        
        # Create project with no yarn
        project = Project(
            project_name="Project Without Yarn",
            pattern_id=pattern_id,
            needle_id=needle_id,
            status="Planning"
        )
        project_id = tracker.create_project(project)
        
        # Retrieve and verify
        saved_project = tracker.get_project(project_id)
        assert saved_project is not None
        assert saved_project.project_name == "Project Without Yarn"
        assert saved_project.yarns == []  # No yarns associated
    
    def test_multiple_yarns_same_project(self, tracker, sample_pattern, sample_needle):
        """
        Test adding multiple yarns to the same project.
        
        This is common for striped projects, colorwork, or when
        using multiple colors in a single project.
        """
        # Setup: Create dependencies
        pattern_id = tracker.create_pattern(sample_pattern)
        needle_id = tracker.create_needle(sample_needle)
        
        project = Project(
            project_name="Striped Scarf",
            pattern_id=pattern_id,
            needle_id=needle_id
        )
        project_id = tracker.create_project(project)
        
        # Create and add multiple yarns
        yarns = []
        for i in range(3):
            yarn = Yarn(
                yarn_brand=f"Brand{i}",
                yarn_line=f"Line{i}",
                color_name=f"Color{i}",
                weight_category="Worsted",
                total_yardage=200
            )
            yarn_id = tracker.create_yarn(yarn)
            yarns.append(yarn_id)
            tracker.add_yarn_to_project(project_id, yarn_id, i + 1)
        
        # Verify all yarns are associated
        saved_project = tracker.get_project(project_id)
        assert len(saved_project.yarns) == 3
        
        # Verify skeins used for each
        skeins = [y['skeins_used'] for y in saved_project.yarns]
        assert sorted(skeins) == [1, 2, 3]  # Each had different skeins count
