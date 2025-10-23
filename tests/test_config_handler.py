"""Unit tests for config_handler module."""

import pytest
import json
import tempfile
import os
from config_handler import save_config, load_config


class TestConfigHandler:
    """Test suite for config handler functions."""

    def test_save_and_load_config(self):
        """Test saving and loading a configuration file."""
        config = {
            "name": "Test Client",
            "city": "NYC",
            "state": "NY",
            "seed_keyword": "SEO",
            "output_root": "./output",
            "niche": "tech",
        }

        # Use temporary file
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            # Save config
            save_config(config, temp_path)

            # Load config
            loaded_config = load_config(temp_path)

            # Verify
            assert loaded_config == config
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_load_nonexistent_file_raises_error(self):
        """Test that loading a non-existent file raises an exception."""
        with pytest.raises(Exception):
            load_config("nonexistent_file.json")

    def test_save_creates_valid_json(self):
        """Test that saved file contains valid JSON."""
        config = {"name": "Test", "value": 123}

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            save_config(config, temp_path)

            # Manually verify JSON is valid
            with open(temp_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                assert loaded == config
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_save_handles_nested_structures(self):
        """Test saving and loading nested data structures."""
        config = {
            "name": "Test",
            "services": ["service1", "service2"],
            "metadata": {"key": "value", "count": 42},
        }

        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        try:
            save_config(config, temp_path)
            loaded_config = load_config(temp_path)

            assert loaded_config == config
            assert loaded_config["services"] == ["service1", "service2"]
            assert loaded_config["metadata"]["count"] == 42
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
