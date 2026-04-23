r"""
Module/Script Name: chatgpt_background_ui.py
Path: E:\projects\Project Tracking\chatgpt_background_ui.py

Description:
Tkinter UI tab for the Business Background Summary Generator. Provides form
inputs for client configuration and triggers GPT-4 background summary generation.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2026-04-23

Last Modified Date:
2026-04-23

Version:
v1.00

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.00 - Initial release with Tkinter UI tab for BackgroundSummaryTab
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox

from chatgpt_background import run


class BackgroundSummaryTab:
    """Tkinter tab interface for the Business Background Summary Generator.

    Provides form inputs for:
    - Business name
    - Business address
    - Website URL
    - Output root directory

    Runs GPT-4 background summary generation in a background thread so the
    GUI remains responsive during API calls.

    Attributes:
        frame: Main ttk.Frame container for the tab.
        name_entry: Entry field for business name.
        address_entry: Entry field for business address.
        url_entry: Entry field for website URL.
        output_root_entry: Entry field for output directory path.
        run_btn: Button to trigger summary generation.
    """

    def __init__(self, parent: tk.Widget) -> None:
        """Initialize the Business Background Summary tab.

        Args:
            parent: Parent Tkinter widget (typically ttk.Notebook).
        """
        self.frame = ttk.Frame(parent)
        self.build_tab()

    def build_tab(self) -> None:
        """Build the tab UI with form inputs and action buttons."""
        row = 0

        ttk.Label(self.frame, text="Business Name:").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.name_entry = ttk.Entry(self.frame, width=60)
        self.name_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="Business Address:").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.address_entry = ttk.Entry(self.frame, width=60)
        self.address_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="Website URL:").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.url_entry = ttk.Entry(self.frame, width=60)
        self.url_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="Output Root Directory:").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.output_root_entry = ttk.Entry(self.frame, width=60)
        self.output_root_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        self.run_btn = ttk.Button(
            self.frame, text="Generate Background Summary", command=self.run_summary
        )
        self.run_btn.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        ttk.Button(self.frame, text="Help", command=self.show_help).grid(
            row=row, column=0, columnspan=2
        )

    def run_summary(self) -> None:
        """Validate inputs and launch background summary generation in a thread.

        Disables the run button during execution to prevent duplicate runs.
        Shows a completion or error dialog when finished.
        """
        name = self.name_entry.get().strip()
        address = self.address_entry.get().strip()
        url = self.url_entry.get().strip()
        output_root = self.output_root_entry.get().strip()

        if not name or not output_root:
            messagebox.showerror(
                "Missing Fields",
                "Business Name and Output Root Directory are required.",
            )
            return

        client_config = {
            "name": name,
            "address": address,
            "url": url,
            "output_root": output_root,
        }

        self.run_btn.config(state="disabled", text="Generating...")

        def task() -> None:
            try:
                run(client_config)
                self.frame.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Complete",
                        f"Background summary saved to:\n{output_root}\\{name}\\",
                    ),
                )
            except Exception as exc:
                err = str(exc)
                self.frame.after(
                    0,
                    lambda: messagebox.showerror("Error", err),
                )
            finally:
                self.frame.after(
                    0,
                    lambda: self.run_btn.config(
                        state="normal", text="Generate Background Summary"
                    ),
                )

        threading.Thread(target=task, daemon=True).start()

    def show_help(self) -> None:
        """Display help dialog explaining the Business Background Summary tool."""
        help_msg = (
            "WHAT THIS DOES:\n"
            "Scrapes your client's website and uses GPT-4 to write a professional\n"
            "business background summary document (DOCX format).\n\n"
            "WHAT YOU NEED TO ENTER:\n"
            "1. Business Name - the client's company name\n"
            "2. Business Address - street address (optional but recommended)\n"
            "3. Website URL - the site to scrape for content (optional)\n"
            "4. Output Root Directory - folder where the DOCX will be saved\n\n"
            "OUTPUT FILE:\n"
            "{Output Root}\\{Business Name}\\{Business Name} background information.docx\n\n"
            "REQUIREMENTS:\n"
            "- OPENAI_API_KEY must be set in your .env file"
        )
        messagebox.showinfo("Background Summary Help", help_msg)

    def get_frame(self) -> ttk.Frame:
        """Return the main frame widget for this tab.

        Returns:
            The ttk.Frame containing all tab UI elements.
        """
        return self.frame
