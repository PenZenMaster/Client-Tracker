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
v1.01

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.01 - Added standardized file header
* v1.00 - Initial logging system with error explanations
"""

import traceback
from datetime import datetime
from tkinter import messagebox

LOG_FILE = "log.txt"


def _timestamp():
    local_tz = datetime.now().astimezone().tzinfo
    return datetime.now(local_tz).strftime("%Y-%m-%d %H:%M:%S")


def log_event(message):
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{_timestamp()}] {message}\n")


def log_error(context, error):
    explanation = explain_error(error)
    error_msg = f"[{_timestamp()}] ERROR in {context}: {repr(error)}\n{traceback.format_exc()}\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(error_msg)
        f.write(f"Explanation: {explanation}\n\n")

    messagebox.showerror(
        f"{context} Failed",
        f"{repr(error)}\n\nExplanation: {explanation}\n\nCheck log.txt for details.",
    )


def explain_error(error):
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
