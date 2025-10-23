"""Unit tests for gmb_keywords module."""

import pytest
import tempfile
import os
from gmb_keywords import run


class TestGMBKeywords:
    """Test suite for GMB keyword generation."""

    def test_generates_keywords_for_single_service(self):
        """Test keyword generation for a single service."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "name": "Test HVAC",
                "services": ["AC Repair"],
                "city": "Phoenix",
                "state": "AZ",
                "output_root": tmpdir
            }

            run(config)

            output_file = os.path.join(tmpdir, "gmb_keywords.txt")
            assert os.path.exists(output_file)

            with open(output_file, "r", encoding="utf-8") as f:
                keywords = f.read().splitlines()

            # Should generate 4 keywords per service
            assert len(keywords) == 4
            assert "Test HVAC Ac Repair Phoenix, AZ" in keywords
            assert "Ac Repair near Phoenix, AZ" in keywords
            assert "Best Ac Repair in Phoenix, AZ" in keywords
            assert "Phoenix, AZ Ac Repair" in keywords

    def test_generates_keywords_for_multiple_services(self):
        """Test keyword generation for multiple services."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "name": "Best Plumbing",
                "services": ["pipe repair", "drain cleaning", "water heater"],
                "city": "Austin",
                "state": "TX",
                "output_root": tmpdir
            }

            run(config)

            output_file = os.path.join(tmpdir, "gmb_keywords.txt")
            with open(output_file, "r", encoding="utf-8") as f:
                keywords = f.read().splitlines()

            # 3 services * 4 keywords each = 12 keywords
            assert len(keywords) == 12

    def test_normalizes_service_names_to_title_case(self):
        """Test that service names are normalized to title case."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "name": "Service Co",
                "services": ["hvac repair", "PLUMBING", "ElEcTrIcAl"],
                "city": "Denver",
                "state": "CO",
                "output_root": tmpdir
            }

            run(config)

            output_file = os.path.join(tmpdir, "gmb_keywords.txt")
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "Hvac Repair" in content
            assert "Plumbing" in content
            assert "Electrical" in content

    def test_strips_whitespace_from_services(self):
        """Test that whitespace is stripped from service names."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "name": "Clean Co",
                "services": ["  cleaning  ", " repair ", "maintenance"],
                "city": "Boston",
                "state": "MA",
                "output_root": tmpdir
            }

            run(config)

            output_file = os.path.join(tmpdir, "gmb_keywords.txt")
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "Cleaning" in content
            assert "Repair" in content

    def test_filters_empty_services(self):
        """Test that empty service strings are filtered out."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "name": "Test Co",
                "services": ["service1", "", "  ", "service2"],
                "city": "Seattle",
                "state": "WA",
                "output_root": tmpdir
            }

            run(config)

            output_file = os.path.join(tmpdir, "gmb_keywords.txt")
            with open(output_file, "r", encoding="utf-8") as f:
                keywords = f.read().splitlines()

            # Only 2 valid services, 4 keywords each = 8 keywords
            assert len(keywords) == 8

    def test_handles_empty_services_list(self):
        """Test behavior with empty services list."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "name": "Empty Services",
                "services": [],
                "city": "Portland",
                "state": "OR",
                "output_root": tmpdir
            }

            run(config)

            output_file = os.path.join(tmpdir, "gmb_keywords.txt")
            with open(output_file, "r", encoding="utf-8") as f:
                keywords = f.read().splitlines()

            # No services = no keywords (but file should exist)
            assert len(keywords) == 0

    def test_uses_default_output_root_when_missing(self):
        """Test that default output root is used when not specified."""
        config = {
            "name": "Default Test",
            "services": ["service"],
            "city": "Miami",
            "state": "FL"
            # No output_root specified
        }

        run(config)

        # Should create in current directory
        output_file = "./gmb_keywords.txt"
        try:
            assert os.path.exists(output_file)
            with open(output_file, "r", encoding="utf-8") as f:
                keywords = f.read().splitlines()
            assert len(keywords) == 4
        finally:
            # Cleanup
            if os.path.exists(output_file):
                os.remove(output_file)

    def test_combines_city_and_state_in_location(self):
        """Test that city and state are combined correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "name": "Location Test",
                "services": ["test service"],
                "city": "New York",
                "state": "NY",
                "output_root": tmpdir
            }

            run(config)

            output_file = os.path.join(tmpdir, "gmb_keywords.txt")
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            assert "New York, NY" in content

    def test_keyword_patterns_are_correct(self):
        """Test that all 4 keyword patterns are generated correctly."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "name": "ABC Company",
                "services": ["Widget Repair"],
                "city": "Chicago",
                "state": "IL",
                "output_root": tmpdir
            }

            run(config)

            output_file = os.path.join(tmpdir, "gmb_keywords.txt")
            with open(output_file, "r", encoding="utf-8") as f:
                keywords = f.read().splitlines()

            # Check all 4 patterns exist
            assert keywords[0] == "ABC Company Widget Repair Chicago, IL"
            assert keywords[1] == "Widget Repair near Chicago, IL"
            assert keywords[2] == "Best Widget Repair in Chicago, IL"
            assert keywords[3] == "Chicago, IL Widget Repair"

    def test_output_file_has_correct_encoding(self):
        """Test that output file uses UTF-8 encoding."""
        with tempfile.TemporaryDirectory() as tmpdir:
            config = {
                "name": "Café Services",
                "services": ["Café Repair"],
                "city": "San José",
                "state": "CA",
                "output_root": tmpdir
            }

            run(config)

            output_file = os.path.join(tmpdir, "gmb_keywords.txt")

            # Read with UTF-8 encoding
            with open(output_file, "r", encoding="utf-8") as f:
                content = f.read()

            # Special characters should be preserved
            assert "Café" in content
            assert "José" in content
