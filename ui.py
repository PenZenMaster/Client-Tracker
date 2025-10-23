r"""
Module/Script Name: ui.py
Path: E:\projects\Project Tracking\ui.py

Description:
Shared UI utilities and launcher for Rank Rocket SEO Toolkit. Creates tabbed
interface with menu bar, help system, and notebook-based tool organization.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved
Original Authors: Skippy the Magnificent, George Penzenik

Created Date:
2025-04-04

Last Modified Date:
2025-10-23

Version:
v1.05

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.05 - Added type hints and Google-style docstrings
* v1.04 - Added standardized file header
* v1.03 - Added full menu bar with File and Help items
* v1.03 - Menu includes Exit and Keyword Volume Help
* v1.00 - Initial release with tabbed interface
"""

import tkinter as tk
from tkinter import ttk, messagebox
from keyword_volume_ui import KeywordVolumeTab


def launch_ui() -> None:
    """Launch the Rank Rocket SEO Toolkit main GUI application.

    Creates a Tkinter window with tabbed interface containing the Keyword Volume
    Checker tool. Includes menu bar with File (Exit) and Help options.

    The window is 800x600 pixels and includes:
    - Menu bar with File and Help menus
    - Tabbed notebook interface
    - Keyword Volume Checker tab

    Returns:
        None. Runs Tkinter main loop until window is closed.

    Example:
        >>> launch_ui()
        [GUI window opens and runs until user closes it]
    """
    root = tk.Tk()
    root.title("Rank Rocket SEO Toolkit - v1.05")
    root.geometry("800x600")

    def show_help() -> None:
        """Display general help dialog with toolkit overview and menu options."""
        help_msg = (
            "🧠 WHAT THIS TOOLKIT DOES:\n\n"
            "This SEO Toolkit helps you generate background summaries, keyword ideas, and Google Business content —\n"
            "and now includes a tool to get REAL monthly search volume using Google's Keyword Planner.\n\n"
            "📌 MENU OPTIONS:\n"
            "• File → Exit — closes the app\n"
            "• Help → Keyword Volume Help — opens a simple guide for the Keyword tab\n"
        )
        messagebox.showinfo("Help", help_msg)

    def show_keyword_volume_help() -> None:
        """Display help dialog specific to Keyword Volume Checker tool."""
        messagebox.showinfo(
            "Keyword Volume Help",
            "This tab fetches average monthly searches from Google Ads.\n\n"
            "You'll need to enter:\n"
            "- Path to your Google Ads YAML config file\n"
            "- Your Google Customer ID\n"
            "- Your business URL\n"
            "- A list of seed keywords separated by commas\n\n"
            "Results will show monthly search volume for each keyword.",
        )

    # Menu Bar
    menubar = tk.Menu(root)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="Keyword Volume Help", command=show_keyword_volume_help)
    help_menu.add_command(label="General Help", command=show_help)
    menubar.add_cascade(label="Help", menu=help_menu)

    root.config(menu=menubar)

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    keyword_tab = KeywordVolumeTab(notebook)
    notebook.add(keyword_tab.get_frame(), text="Keyword Volume Checker")

    root.mainloop()


if __name__ == "__main__":
    launch_ui()
