"""Unit tests for config_handler module."""

import pytest
import json
import tempfile
import os
from unittest.mock import patch
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

    @patch('logger.messagebox.showerror')
    def test_load_nonexistent_file_raises_error(self, mock_msgbox):
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

    @patch('config_handler.filedialog.asksaveasfilename')
    def test_save_config_without_filename_uses_dialog(self, mock_dialog):
        """Test that save_config opens dialog when filename not provided."""
        mock_dialog.return_value = None  # User cancels dialog

        config = {"name": "Test"}

        # Should not raise error when user cancels
        save_config(config, filename=None)

        # Verify dialog was called
        mock_dialog.assert_called_once()

    @patch('config_handler.filedialog.asksaveasfilename')
    def test_save_config_dialog_with_user_selection(self, mock_dialog):
        """Test save_config saves to user-selected path from dialog."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            temp_path = f.name

        mock_dialog.return_value = temp_path

        try:
            config = {"name": "Dialog Test", "value": 123}
            save_config(config, filename=None)

            # Verify file was saved
            loaded = load_config(temp_path)
            assert loaded == config
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    @patch('logger.messagebox.showerror')
    def test_load_config_with_malformed_json(self, mock_msgbox):
        """Test that load_config handles malformed JSON gracefully."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
            f.write("{invalid json content")
            temp_path = f.name

        try:
            with pytest.raises(Exception):  # Should raise JSON decode error
                load_config(temp_path)
        finally:
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    @patch('config_handler.log_error')
    def test_save_config_logs_errors(self, mock_log_error):
        """Test that save_config logs errors when they occur."""
        # Try to save to invalid path
        invalid_path = "/invalid/path/that/does/not/exist/config.json"
        config = {"name": "Test"}

        with pytest.raises(Exception):
            save_config(config, invalid_path)

        # Verify log_error was called
        mock_log_error.assert_called_once()
        assert mock_log_error.call_args[0][0] == "Save Config"

    @patch('config_handler.log_error')
    def test_load_config_logs_errors(self, mock_log_error):
        """Test that load_config logs errors when they occur."""
        with pytest.raises(Exception):
            load_config("nonexistent_file_xyz123.json")

        # Verify log_error was called
        mock_log_error.assert_called_once()
        assert mock_log_error.call_args[0][0] == "Load Config"
