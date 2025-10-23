r"""
Module/Script Name: main.py
Path: E:\projects\Project Tracking\main.py

Description:
Main GUI launcher for Rank Rocket SEO Toolkit. Creates tabbed interface with
Keyword Volume Checker, Business Description Generator, GMB Keyword Generator,
and FAQ Generator tools.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2025-04-03

Last Modified Date:
2025-10-23

Version:
v1.12

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.12 - Added type hints and Google-style docstrings
* v1.11 - Added standardized file header and version display in title
* v1.10 - Full GUI launcher with all available Skippy tools
"""

import tkinter as tk
from tkinter import ttk
from keyword_volume_ui import KeywordVolumeTab
from run_chatgpt_background import BackgroundSummaryTab  # type: ignore[attr-defined]
from run_gmb_keywords import GMBKeywordTab  # type: ignore[attr-defined]
from run_faq_generator import FAQTab  # type: ignore[attr-defined]
from logger import log_event


def launch_ui() -> None:
    """Launch the main Rank Rocket SEO Toolkit GUI application.

    Creates a Tkinter window with 800x600 pixel dimensions and tabbed notebook
    interface containing four SEO tools:
    1. Keyword Volume Checker - Google Ads API keyword research
    2. Business Description Generator - GPT-4 business summaries
    3. GMB Keyword Generator - Google Business Profile keyword variants
    4. FAQ Generator - SerpAPI + GPT-4 FAQ content creation

    Each tab is dynamically loaded and logged on initialization.

    Returns:
        None. Runs Tkinter main loop until application is closed.

    Example:
        >>> launch_ui()
        [GUI window opens with 4 tabs and runs until closed]

    Note:
        Tab loading events are logged to log.txt via logger module.
    """
    root = tk.Tk()
    root.title("Rank Rocket: Skippy's SEO Toolkit v1.12")
    root.geometry("800x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    tabs = [
        ("Keyword Volume Checker", KeywordVolumeTab),
        ("Business Description Generator", BackgroundSummaryTab),
        ("GMB Keyword Generator", GMBKeywordTab),
        ("FAQ Generator", FAQTab),
    ]

    for label, tab_class in tabs:
        log_event(f"Loading tab: {label}")
        tab = tab_class(notebook)
        notebook.add(tab.get_frame(), text=label)

    root.mainloop()


if __name__ == "__main__":
    launch_ui()
