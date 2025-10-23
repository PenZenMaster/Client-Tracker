"""Unit tests for city_utils module."""

import pytest
from city_utils import handle_city_inputs


class TestHandleCityInputs:
    """Test suite for handle_city_inputs function."""

    def test_basic_city_expansion(self):
        """Test that city variations are generated correctly."""
        config = {"city": "Springfield"}
        result = handle_city_inputs(config)

        assert "nearby_10mi" in result
        assert "nearby_20mi" in result
        assert len(result["nearby_10mi"]) == 2
        assert len(result["nearby_20mi"]) == 2

    def test_10mi_cities_contain_base_city(self):
        """Test that 10mi variations contain the base city name."""
        config = {"city": "Portland"}
        result = handle_city_inputs(config)

        for city in result["nearby_10mi"]:
            assert "Portland" in city

    def test_20mi_cities_contain_base_city(self):
        """Test that 20mi variations contain the base city name."""
        config = {"city": "Austin"}
        result = handle_city_inputs(config)

        for city in result["nearby_20mi"]:
            assert "Austin" in city

    def test_missing_city_field(self):
        """Test behavior when city field is missing."""
        config = {}
        result = handle_city_inputs(config)

        # Should still create nearby fields with empty strings
        assert "nearby_10mi" in result
        assert "nearby_20mi" in result

    def test_empty_city_string(self):
        """Test behavior with empty city string."""
        config = {"city": ""}
        result = handle_city_inputs(config)

        assert result["nearby_10mi"] == [" Heights", " North"]
        assert result["nearby_20mi"] == [" Valley", " Junction"]

    def test_original_config_preserved(self):
        """Test that original config fields are preserved."""
        config = {"city": "Boston", "state": "MA", "name": "Test Business"}
        result = handle_city_inputs(config)

        assert result["city"] == "Boston"
        assert result["state"] == "MA"
        assert result["name"] == "Test Business"

    def test_config_modified_in_place(self):
        """Test that config is modified in place and returned."""
        config = {"city": "Seattle"}
        result = handle_city_inputs(config)

        # Should be the same object
        assert result is config
        assert "nearby_10mi" in config
        assert "nearby_20mi" in config
