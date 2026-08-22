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