"""
============================================================
Unit Tests for the Data Models Module
============================================================
These tests verify that the dataclass models correctly initialize,
handle default values, and maintain data integrity.

Author: Anna Khoriakova
Last Updated: 2026-08-21
============================================================
"""

import pytest
from datetime import date
from src.models import Pattern, Needle, Yarn, Project


class TestPattern:
    """
    Test suite for the Pattern model.
    
    Tests cover:
    - Creating patterns with all fields
    - Creating patterns with minimal fields
    - Default values when fields are omitted
    """
    
    def test_create_pattern_with_all_fields(self):
        """
        Test creating a Pattern with all fields provided.
        
        Verifies that:
        - All fields are correctly assigned during initialization
        - No fields are accidentally set to None or default values
        """
        # Create a pattern with complete information
        pattern = Pattern(
            pattern_id=1,
            pattern_name="Aran Sweater",
            designer="Alice Starmore"
        )
        
        # Assert all fields were set correctly
        assert pattern.pattern_id == 1
        assert pattern.pattern_name == "Aran Sweater"
        assert pattern.designer == "Alice Starmore"
    
    def test_create_pattern_with_minimal_fields(self):
        """
        Test creating a Pattern with only required fields.
        
        Verifies that:
        - Pattern can be created without a designer
        - Pattern ID is None for new (unsaved) patterns
        - Only the required field (pattern_name) must be provided
        """
        # Create a pattern with just the name
        pattern = Pattern(pattern_name="Simple Scarf")
        
        # Assert required field was set
        assert pattern.pattern_id is None  # New pattern, not yet saved
        assert pattern.pattern_name == "Simple Scarf"
        assert pattern.designer is None   # Optional field remains None
    
    def test_create_pattern_with_defaults(self):
        """
        Test Pattern default values when no fields provided.
        
        Verifies that:
        - All fields have defaults
        - Optional fields are None
        - Required fields are empty strings (not None)
        """
        # Create a pattern with no arguments (all defaults)
        pattern = Pattern()
        
        # Assert all defaults are correct
        assert pattern.pattern_id is None
        assert pattern.pattern_name == ""  # Empty string, not None
        assert pattern.designer is None

class TestNeedle:
    """
    Test suite for the Needle model.
    
    Tests cover:
    - Creating needles with all physical attributes
    - Creating needles with only essential information
    """
    
    def test_create_needle_with_all_fields(self):
        """
        Test creating a Needle with all fields provided.
        
        Verifies that:
        - All needle attributes are correctly stored
        - Size is stored as a float (supports decimal sizes like 3.75mm)
        - Type, material, length, and brand are all saved
        """
        # Create a needle with complete specifications
        needle = Needle(
            needle_id=1,
            needle_size_mm=4.0,
            needle_type="Circular",
            needle_material="Metal",
            needle_length="24",
            needle_brand="KnitPro"
        )
        
        # Assert all fields were set correctly
        assert needle.needle_id == 1
        assert needle.needle_size_mm == 4.0
        assert needle.needle_type == "Circular"
        assert needle.needle_material == "Metal"
        assert needle.needle_length == "24"
        assert needle.needle_brand == "KnitPro"
    
    def test_create_needle_with_minimal_fields(self):
        """
        Test creating a Needle with only required fields.
        
        Verifies that:
        - Needle can be created with just size and type
        - All other attributes are optional and default to None
        - Common for patterns that specify size but not brand/material
        """
        # Create a needle with just the essential information
        needle = Needle(needle_size_mm=5.5, needle_type="DPN")
        
        # Assert required fields were set
        assert needle.needle_size_mm == 5.5
        assert needle.needle_type == "DPN"
        
        # Assert optional fields are None (not set)
        assert needle.needle_material is None
        assert needle.needle_length is None
        assert needle.needle_brand is None

class TestYarn:
    """
    Test suite for the Yarn model.
    
    Tests cover:
    - Creating yarn with complete specifications
    - Creating yarn with just brand name
    """
    
    def test_create_yarn_with_all_fields(self):
        """
        Test creating a Yarn with all fields provided.
        
        Verifies that:
        - All yarn attributes are correctly stored
        - Dye lot is preserved (important for colour matching)
        - Yardage is stored as integer for calculations
        - Weight category is stored for gauge matching
        """
        # Create a yarn with complete details
        yarn = Yarn(
            yarn_id=1,
            yarn_brand="Malabrigo",
            yarn_line="Rios",
            colour_name="Whale's Road",
            dye_lot="12345",
            weight_category="Worsted",
            total_yardage=210
        )
        
        # Assert all fields were set correctly
        assert yarn.yarn_id == 1
        assert yarn.yarn_brand == "Malabrigo"
        assert yarn.yarn_line == "Rios"
        assert yarn.colour_name == "Whale's Road"
        assert yarn.dye_lot == "12345"
        assert yarn.weight_category == "Worsted"
        assert yarn.total_yardage == 210
    
    def test_create_yarn_with_minimal_fields(self):
        """
        Test creating a Yarn with only the required brand.
        
        Verifies that:
        - Brand is the only required field
        - All other details can be added later
        - This is useful when you know the brand but not the specific line yet
        """
        # Create a yarn with just the brand name
        yarn = Yarn(yarn_brand="Cascade")
        
        # Assert brand was set
        assert yarn.yarn_brand == "Cascade"
        
        # Assert all other fields are None (not set yet)
        assert yarn.yarn_line is None
        assert yarn.colour_name is None
        assert yarn.dye_lot is None
        assert yarn.weight_category is None
        assert yarn.total_yardage is None

class TestProject:
    """
    Test suite for the Project model.
    
    Tests cover:
    - Creating complete projects with all fields
    - Creating projects with minimal information
    - Default status behavior
    - Post-initialization handling of yarns list
    """
    
    def test_create_project_with_all_fields(self):
        """
        Test creating a Project with all fields provided.
        
        Verifies that:
        - All project fields are correctly assigned
        - Associated yarns are stored as a list
        - Dates are stored as strings (ISO format)
        - Foreign key references (pattern_id, needle_id) are preserved
        """
        # Create a yarn to associate with the project
        project_yarn = Yarn(yarn_brand="Malabrigo")
        
        # Create a project with complete information
        project = Project(
            project_id=1,
            project_name="My Aran Sweater",
            start_date="2026-08-21",
            end_date=None,  # Project is still in progress
            status="WIP",
            recipient="Me",
            pattern_id=1,
            needle_id=2,
            yarns=[project_yarn]  # Associate yarn with project
        )
        
        # Assert all fields were set correctly
        assert project.project_id == 1
        assert project.project_name == "My Aran Sweater"
        assert project.start_date == "2026-08-21"
        assert project.end_date is None  # In progress project
        assert project.status == "WIP"
        assert project.recipient == "Me"
        assert project.pattern_id == 1
        assert project.needle_id == 2
        assert len(project.yarns) == 1
        assert project.yarns[0].yarn_brand == "Malabrigo"
    
    def test_create_project_with_minimal_fields(self):
        """
        Test creating a Project with only required fields.
        
        Verifies that:
        - Only name, pattern_id, and needle_id are required
        - Status defaults to 'Planning' automatically
        - All date fields are None for new projects
        - yarns is initialized as empty list by __post_init__
        """
        # Create a project with just the essentials
        project = Project(
            project_name="Simple Hat",
            pattern_id=1,
            needle_id=2
        )
        
        # Assert required fields were set
        assert project.project_name == "Simple Hat"
        assert project.pattern_id == 1
        assert project.needle_id == 2
        
        # Assert defaults are applied correctly
        assert project.status == "Planning"  # Default status
        assert project.start_date is None    # No start date set
        assert project.end_date is None      # No end date set
        assert project.recipient is None     # No recipient specified
        assert project.yarns == []           # __post_init__ ensures empty list
    
    def test_project_default_status(self):
        """
        Test that Project status defaults to 'Planning'.
        """
        # Create project without specifying status
        project = Project(project_name="Test", pattern_id=1, needle_id=1)
        
        # Assert default status is 'Planning'
        assert project.status == "Planning"
    
    def test_project_yarns_post_init(self):
        """
        Test that __post_init__ ensures yarns is always a list.
        
        Three scenarios are tested:
        1. yarns=None (explicitly passed as None)
        2. yarns not provided at all (uses default)
        3. yarns already a list (should remain unchanged)
        """
        # Scenario 1: yarns explicitly set to None
        project1 = Project(
            project_name="Test1",
            pattern_id=1,
            needle_id=1,
            yarns=None  # Explicitly None
        )
        # __post_init__ should convert this to empty list
        assert project1.yarns == []
        
        # Scenario 2: yarns not provided (uses default None from signature)
        project2 = Project(project_name="Test2", pattern_id=1, needle_id=1)
        # __post_init__ should initialize as empty list
        assert project2.yarns == []
        
        # Scenario 3: yarns already a list (should stay as-is)
        yarns = [Yarn(yarn_brand="Test")]
        project3 = Project(
            project_name="Test3",
            pattern_id=1,
            needle_id=1,
            yarns=yarns  # Already a list
        )
        # __post_init__ should not modify an existing list
        assert project3.yarns == yarns
