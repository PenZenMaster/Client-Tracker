r"""
Module/Script Name: config_handler.py
Path: E:\projects\Project Tracking\config_handler.py

Description:
Configuration file I/O utilities for JSON-based client configs. Handles
loading and saving configuration files with file dialogs and error logging.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2024-01-15

Last Modified Date:
2025-10-23

Version:
v1.02

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.02 - Added type hints and Google-style docstrings
* v1.01 - Added standardized file header
* v1.00 - Initial release with JSON config handling
"""

import os
import json
from typing import Dict, Any, Optional
from tkinter import filedialog
from logger import log_error

DEFAULT_FILENAME = "client_config.json"


def save_config(config: Dict[str, Any], filename: Optional[str] = None) -> None:
    """Save client configuration to JSON file.

    Opens a file dialog if filename is not provided. Logs errors and re-raises
    exceptions for upstream handling.

    Args:
        config: Dictionary containing client configuration data.
        filename: Optional path to save file. If None, opens save dialog.

    Raises:
        Exception: Re-raises any exceptions after logging them.

    Example:
        >>> config = {"name": "Test Client", "city": "NYC"}
        >>> save_config(config, "client.json")
    """
    try:
        if not filename:
            filename = filedialog.asksaveasfilename(
                defaultextension=".json",
                initialdir=os.getcwd(),
                filetypes=[("JSON files", "*.json")],
                title="Save Configuration As",
            )
        if filename:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
    except Exception as e:
        log_error("Save Config", e)
        raise


def load_config(filepath: str) -> Dict[str, Any]:
    """Load client configuration from JSON file.

    Args:
        filepath: Path to the JSON configuration file.

    Returns:
        Dictionary containing the loaded configuration data.

    Raises:
        Exception: Re-raises any exceptions after logging them.

    Example:
        >>> config = load_config("client.json")
        >>> print(config["name"])
        'Test Client'
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log_error("Load Config", e)
        raise
