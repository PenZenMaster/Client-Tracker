# Author: Skippy the Magnificent along with that dumb ape, George Penzenik
# Version: 1.03
# Date Modified: 00:12 04/04/2025
# Comment:
#  - Added full menu bar with File and Help items for meat sack clarity
#  - Menu includes Exit and Keyword Volume Help

import tkinter as tk
from tkinter import ttk, messagebox
from keyword_volume_ui import KeywordVolumeTab

def launch_ui():
    root = tk.Tk()
    root.title("Rank Rocket SEO Toolkit - v1.03")
    root.geometry("800x600")

    def show_help():
        help_msg = (
            "🧠 WHAT THIS TOOLKIT DOES:\n\n"
            "This SEO Toolkit helps you generate background summaries, keyword ideas, and Google Business content —\n"
            "and now includes a tool to get REAL monthly search volume using Google's Keyword Planner.\n\n"
            "📌 MENU OPTIONS:\n"
            "• File → Exit — closes the app\n"
            "• Help → Keyword Volume Help — opens a simple guide for the Keyword tab\n"
        )
        messagebox.showinfo("Help", help_msg)

    def show_keyword_volume_help():
        messagebox.showinfo("Keyword Volume Help",
            "This tab fetches average monthly searches from Google Ads.\n\n"
            "You'll need to enter:\n"
            "- Path to your Google Ads YAML config file\n"
            "- Your Google Customer ID\n"
            "- Your business URL\n"
            "- A list of seed keywords separated by commas\n\n"
            "Results will show monthly search volume for each keyword.")

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
