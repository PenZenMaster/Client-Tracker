# logger.py
import traceback
from datetime import datetime
import pytz
import os
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

    messagebox.showerror(f"{context} Failed", f"{repr(error)}\n\nExplanation: {explanation}\n\nCheck log.txt for details.")

def explain_error(error):
    if isinstance(error, KeyError):
        return "A required field may be missing. Double-check your configuration values."
    elif isinstance(error, FileNotFoundError):
        return "File not found. Make sure the file exists and the path is correct."
    elif isinstance(error, ValueError):
        return "Invalid input. Ensure that numbers or formats are entered correctly."
    else:
        return "An unexpected error occurred. Try again or check log.txt for details."
