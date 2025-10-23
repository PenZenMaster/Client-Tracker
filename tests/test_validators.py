"""Unit tests for validators module."""

import pytest
from validators import validate_config


class TestValidateConfig:
    """Test suite for validate_config function."""

    def test_valid_config_passes(self):
        """Test that a valid configuration passes validation."""
        config = {
            "name": "Test Business",
            "city": "New York",
            "state": "NY",
            "seed_keyword": "SEO services",
            "output_root": "./output",
            "niche": "technology",
        }
        # Should not raise any exception
        validate_config(config)

    def test_missing_single_field_raises_error(self):
        """Test that missing a single required field raises KeyError."""
        config = {
            "name": "Test Business",
            "city": "New York",
            "state": "NY",
            "seed_keyword": "SEO services",
            "output_root": "./output",
            # Missing 'niche'
        }
        with pytest.raises(KeyError, match="Missing required fields: niche"):
            validate_config(config)

    def test_missing_multiple_fields_raises_error(self):
        """Test that missing multiple required fields raises KeyError."""
        config = {
            "name": "Test Business",
            "city": "New York",
            # Missing state, seed_keyword, output_root, niche
        }
        with pytest.raises(KeyError, match="Missing required fields"):
            validate_config(config)

    def test_empty_dict_raises_error(self):
        """Test that an empty configuration dict raises KeyError."""
        config = {}
        with pytest.raises(KeyError, match="Missing required fields"):
            validate_config(config)

    def test_extra_fields_allowed(self):
        """Test that extra fields in config are allowed."""
        config = {
            "name": "Test Business",
            "city": "New York",
            "state": "NY",
            "seed_keyword": "SEO services",
            "output_root": "./output",
            "niche": "technology",
            "extra_field": "extra_value",  # Extra field
            "another_extra": 123,
        }
        # Should not raise any exception
        validate_config(config)
