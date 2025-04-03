# Author: Skippy the Magnificent along with that dumb ape, George Penzenik
# Version: 1.01
# Date Modified: 23:52 04/03/2025
# Comment:
#  - Added UI tab for Keyword Volume Fetcher
#  - Provides help text in Barney-style clarity for meat sacks

import tkinter as tk
from tkinter import ttk, messagebox
from keyword_volume import fetch_keyword_ideas
from google.ads.googleads.client import GoogleAdsClient

class KeywordVolumeTab:
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.build_tab()

    def build_tab(self):
        row = 0

        ttk.Label(self.frame, text="🔧 Google Ads YAML Config Path:").grid(row=row, column=0, sticky="e", pady=5, padx=5)
        self.config_path_entry = ttk.Entry(self.frame, width=60)
        self.config_path_entry.insert(0, "google-ads.yaml")
        self.config_path_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="🧾 Google Customer ID:").grid(row=row, column=0, sticky="e", pady=5, padx=5)
        self.customer_id_entry = ttk.Entry(self.frame, width=40)
        self.customer_id_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="🌐 Business Page URL:").grid(row=row, column=0, sticky="e", pady=5, padx=5)
        self.url_entry = ttk.Entry(self.frame, width=60)
        self.url_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="🔍 Seed Keywords (comma-separated):").grid(row=row, column=0, sticky="e", pady=5, padx=5)
        self.keywords_entry = ttk.Entry(self.frame, width=60)
        self.keywords_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        self.fetch_btn = ttk.Button(self.frame, text="Fetch Keyword Volume", command=self.fetch_volume)
        self.fetch_btn.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        self.help_btn = ttk.Button(self.frame, text="Help", command=self.show_help)
        self.help_btn.grid(row=row, column=0, columnspan=2)

    def fetch_volume(self):
        try:
            config_path = self.config_path_entry.get().strip()
            customer_id = self.customer_id_entry.get().strip()
            page_url = self.url_entry.get().strip()
            keywords = [k.strip() for k in self.keywords_entry.get().split(",") if k.strip()]

            if not all([config_path, customer_id, page_url, keywords]):
                raise ValueError("Please fill out ALL fields before fetching keyword volume.")

            client = GoogleAdsClient.load_from_storage(config_path)
            results = fetch_keyword_ideas(client, customer_id, page_url, keywords)

            result_str = "\n".join([f"{kw}: {vol} searches/month" for kw, vol in results])
            messagebox.showinfo("Keyword Volume Results", result_str)

        except Exception as e:
            messagebox.showerror("Error Fetching Keywords", str(e))

    def show_help(self):
        help_msg = (
            "🧠 WHAT THIS DOES:\n"
            "This tool checks how many people are searching for your chosen keywords using Google Ads' Keyword Planner.\n\n"
            "🧾 WHAT YOU NEED TO ENTER:\n"
            "1. Google Ads YAML Config Path — the file that holds your API keys\n"
            "2. Google Customer ID — looks like a 10-digit number (e.g., 123-456-7890)\n"
            "3. Business URL — the page you're trying to rank (e.g., your homepage or service page)\n"
            "4. Seed Keywords — like 'furnace repair', 'AC install', etc. Use commas to separate them\n\n"
            "🎯 WHAT YOU GET BACK:\n"
            "A list of keywords plus their average monthly search volume\n\n"
            "If you're still confused, ask Skippy."
        )
        messagebox.showinfo("Keyword Volume Help", help_msg)

    def get_frame(self):
        return self.frame
