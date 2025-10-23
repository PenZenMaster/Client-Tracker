r"""
Module/Script Name: logger.py
Path: E:\projects\Project Tracking\logger.py

Description:
Logging system with timestamped event/error tracking and user-friendly error
explanations. Writes to log.txt and displays error dialogs.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2025-04-03

Last Modified Date:
2025-10-22

Version:
v1.02

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.02 - Added type hints and Google-style docstrings
* v1.01 - Added standardized file header
* v1.00 - Initial logging system with error explanations
"""

import traceback
from datetime import datetime
from tkinter import messagebox
from typing import Any

LOG_FILE = "log.txt"


def _timestamp() -> str:
    """Generate timestamp string for log entries.

    Returns:
        Formatted timestamp string in YYYY-MM-DD HH:MM:SS format with local timezone.
    """
    local_tz = datetime.now().astimezone().tzinfo
    return datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")


def log_event(message: str) -> None:
    """Log an event message to the log file with timestamp.

    Args:
        message: Event message to log.

    Example:
        >>> log_event("Application started successfully")
    """
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{_timestamp()}] {message}\n")


def log_error(context: str, error: Exception) -> None:
    """Log an error with context, traceback, and user-friendly explanation.

    Writes error details to log file and displays error dialog to user.

    Args:
        context: Description of where the error occurred (e.g., "Load Config").
        error: The exception that was raised.

    Example:
        >>> try:
        ...     raise ValueError("Invalid input")
        ... except ValueError as e:
        ...     log_error("Input Validation", e)
    """
    explanation = explain_error(error)
    error_msg = f"[{_timestamp()}] ERROR in {context}: {repr(error)}\n{traceback.format_exc()}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(error_msg)
        f.write(f"Explanation: {explanation}\n\n")

    messagebox.showerror(
        f"{context} Failed",
        f"{repr(error)}\n\nExplanation: {explanation}\n\nCheck log.txt for details.",
    )


def explain_error(error: Exception) -> str:
    """Generate user-friendly explanation for common error types.

    Args:
        error: The exception to explain.

    Returns:
        User-friendly error explanation string.

    Example:
        >>> error = KeyError("missing_field")
        >>> explain_error(error)
        'A required field may be missing. Double-check your configuration values.'
    """
    if isinstance(error, KeyError):
        return (
            "A required field may be missing. Double-check your configuration values."
        )
    elif isinstance(error, FileNotFoundError):
        return "File not found. Make sure the file exists and the path is correct."
    elif isinstance(error, ValueError):
        return "Invalid input. Ensure that numbers or formats are entered correctly."
    else:
        return "An unexpected error occurred. Try again or check log.txt for details."
