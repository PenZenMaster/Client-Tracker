"""Unit tests for logger module."""

import tempfile
import os
from unittest.mock import patch
from logger import log_event, log_error, explain_error


class TestLogger:
    """Test suite for logging functions."""

    def test_log_event_writes_to_file(self):
        """Test that log_event writes message to log file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_log = f.name

        try:
            with patch("logger.LOG_FILE", temp_log):
                log_event("Test event message")

            with open(temp_log, "r", encoding="utf-8") as f:
                content = f.read()

            assert "Test event message" in content
            assert "]" in content  # Timestamp format check
        finally:
            if os.path.exists(temp_log):
                os.unlink(temp_log)

    def test_log_event_includes_timestamp(self):
        """Test that log_event includes timestamp."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_log = f.name

        try:
            with patch("logger.LOG_FILE", temp_log):
                log_event("Timestamped event")

            with open(temp_log, "r", encoding="utf-8") as f:
                content = f.read()

            # Check for timestamp format [YYYY-MM-DD HH:MM:SS]
            assert "[" in content
            assert "]" in content
            assert "Timestamped event" in content
        finally:
            if os.path.exists(temp_log):
                os.unlink(temp_log)

    @patch("logger.messagebox.showerror")
    def test_log_error_writes_error_to_file(self, mock_msgbox):
        """Test that log_error writes error details to log file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_log = f.name

        try:
            with patch("logger.LOG_FILE", temp_log):
                error = ValueError("Test error")
                log_error("Test Context", error)

            with open(temp_log, "r", encoding="utf-8") as f:
                content = f.read()

            assert "ERROR in Test Context" in content
            assert "ValueError" in content
            assert "Explanation:" in content
        finally:
            if os.path.exists(temp_log):
                os.unlink(temp_log)

    @patch("logger.messagebox.showerror")
    def test_log_error_shows_message_box(self, mock_msgbox):
        """Test that log_error displays error message box."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_log = f.name

        try:
            with patch("logger.LOG_FILE", temp_log):
                error = KeyError("missing_key")
                log_error("Config Error", error)

            # Verify messagebox was called
            mock_msgbox.assert_called_once()
            args = mock_msgbox.call_args

            assert "Config Error Failed" in args[0]
            assert "KeyError" in str(args[0])
        finally:
            if os.path.exists(temp_log):
                os.unlink(temp_log)

    def test_explain_error_key_error(self):
        """Test error explanation for KeyError."""
        error = KeyError("missing_field")
        explanation = explain_error(error)

        assert "required field may be missing" in explanation
        assert "configuration" in explanation

    def test_explain_error_file_not_found(self):
        """Test error explanation for FileNotFoundError."""
        error = FileNotFoundError("file.txt not found")
        explanation = explain_error(error)

        assert "File not found" in explanation
        assert "path is correct" in explanation

    def test_explain_error_value_error(self):
        """Test error explanation for ValueError."""
        error = ValueError("invalid value")
        explanation = explain_error(error)

        assert "Invalid input" in explanation
        assert "numbers or formats" in explanation

    def test_explain_error_generic_exception(self):
        """Test error explanation for generic exception."""
        error = RuntimeError("unexpected error")
        explanation = explain_error(error)

        assert "unexpected error occurred" in explanation
        assert "log.txt" in explanation

    def test_explain_error_custom_exception(self):
        """Test error explanation for custom exception type."""

        class CustomError(Exception):
            pass

        error = CustomError("custom error")
        explanation = explain_error(error)

        # Should return generic message for unknown error types
        assert "unexpected error occurred" in explanation

    @patch("logger.messagebox.showerror")
    def test_log_error_includes_traceback(self, mock_msgbox):
        """Test that log_error includes full traceback."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_log = f.name

        try:
            with patch("logger.LOG_FILE", temp_log):
                try:
                    raise ValueError("Test error with traceback")
                except ValueError as e:
                    log_error("Traceback Test", e)

            with open(temp_log, "r", encoding="utf-8") as f:
                content = f.read()

            # Traceback should be present
            assert "Traceback" in content or "ValueError" in content
        finally:
            if os.path.exists(temp_log):
                os.unlink(temp_log)

    def test_log_event_appends_to_existing_file(self):
        """Test that log_event appends to existing log file."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_log = f.name

        try:
            with patch("logger.LOG_FILE", temp_log):
                log_event("First message")
                log_event("Second message")

            with open(temp_log, "r", encoding="utf-8") as f:
                lines = f.readlines()

            # Should have two log entries
            assert len(lines) >= 2
            assert any("First message" in line for line in lines)
            assert any("Second message" in line for line in lines)
        finally:
            if os.path.exists(temp_log):
                os.unlink(temp_log)

    @patch("logger.messagebox.showerror")
    def test_log_error_message_box_content(self, mock_msgbox):
        """Test that error message box contains correct information."""
        with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".txt") as f:
            temp_log = f.name

        try:
            with patch("logger.LOG_FILE", temp_log):
                error = FileNotFoundError("config.json")
                log_error("File Load", error)

            # Check message box call arguments
            call_args = mock_msgbox.call_args[0]
            assert "File Load Failed" == call_args[0]
            assert "FileNotFoundError" in call_args[1]
            assert "Explanation:" in call_args[1]
            assert "log.txt" in call_args[1]
        finally:
            if os.path.exists(temp_log):
                os.unlink(temp_log)
