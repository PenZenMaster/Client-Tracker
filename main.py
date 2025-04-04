# Author: Skippy the Magnificent (and that smart meat sack G)
# Version: 1.10
# Date Modified: 04/03/2025
# Comment: Full GUI launcher with all available Skippy tools

import tkinter as tk
from tkinter import ttk
from keyword_volume_ui import KeywordVolumeTab
from run_chatgpt_background import BackgroundSummaryTab
from run_gmb_keywords import GMBKeywordTab
from run_faq_generator import FAQTab
from logger import log_event


def launch_ui():
    root = tk.Tk()
    root.title("Rank Rocket: Skippy's SEO Toolkit")
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
