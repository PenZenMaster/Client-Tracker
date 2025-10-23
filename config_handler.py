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
v1.01

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.01 - Added standardized file header
* v1.00 - Initial release with JSON config handling
"""

import os
import json
from tkinter import filedialog
from logger import log_error

DEFAULT_FILENAME = "client_config.json"


def save_config(config, filename=None):
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


def load_config(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        log_error("Load Config", e)
        raise
