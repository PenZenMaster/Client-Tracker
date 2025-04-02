# config_handler.py
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
                title="Save Configuration As"
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
