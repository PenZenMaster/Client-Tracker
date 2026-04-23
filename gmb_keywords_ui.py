r"""
Module/Script Name: gmb_keywords_ui.py
Path: E:\projects\Project Tracking\gmb_keywords_ui.py

Description:
Tkinter UI tab for the GMB Keyword Generator. Provides form inputs for client
configuration and triggers Google Business Profile keyword variant generation.

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
* v1.00 - Initial release with Tkinter UI tab for GMBKeywordTab
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox

from gmb_keywords import run


class GMBKeywordTab:
    """Tkinter tab interface for the GMB Keyword Generator.

    Provides form inputs for:
    - Business name
    - Services (comma-separated)
    - City
    - State abbreviation
    - Output root directory

    Runs keyword generation in a background thread so the GUI remains
    responsive during file I/O.

    Attributes:
        frame: Main ttk.Frame container for the tab.
        name_entry: Entry field for business name.
        services_entry: Entry field for comma-separated services.
        city_entry: Entry field for city name.
        state_entry: Entry field for state abbreviation.
        output_root_entry: Entry field for output directory path.
        run_btn: Button to trigger keyword generation.
    """

    def __init__(self, parent: tk.Widget) -> None:
        """Initialize the GMB Keyword Generator tab.

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

        ttk.Label(self.frame, text="Services (comma-separated):").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.services_entry = ttk.Entry(self.frame, width=60)
        self.services_entry.insert(0, "AC repair, furnace install, heating")
        self.services_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="City:").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.city_entry = ttk.Entry(self.frame, width=40)
        self.city_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="State (abbreviation):").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.state_entry = ttk.Entry(self.frame, width=10)
        self.state_entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="Output Root Directory:").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.output_root_entry = ttk.Entry(self.frame, width=60)
        self.output_root_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        self.run_btn = ttk.Button(
            self.frame, text="Generate GMB Keywords", command=self.run_keywords
        )
        self.run_btn.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        ttk.Button(self.frame, text="Help", command=self.show_help).grid(
            row=row, column=0, columnspan=2
        )

    def run_keywords(self) -> None:
        """Validate inputs and launch GMB keyword generation in a thread.

        Disables the run button during execution to prevent duplicate runs.
        Shows a completion or error dialog when finished.
        """
        name = self.name_entry.get().strip()
        services_raw = self.services_entry.get().strip()
        city = self.city_entry.get().strip()
        state = self.state_entry.get().strip()
        output_root = self.output_root_entry.get().strip()

        if not all([name, services_raw, city, state]):
            messagebox.showerror(
                "Missing Fields",
                "Business Name, Services, City, and State are all required.",
            )
            return

        services = [s.strip() for s in services_raw.split(",") if s.strip()]

        client_config = {
            "name": name,
            "services": services,
            "city": city,
            "state": state,
            "output_root": output_root or ".",
        }

        self.run_btn.config(state="disabled", text="Generating...")

        def task() -> None:
            try:
                run(client_config)
                self.frame.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Complete",
                        f"GMB keywords saved to:\n{client_config['output_root']}\\{name}\\gmb_keywords.txt",
                    ),
                )
            except Exception as exc:
                err = str(exc)
                self.frame.after(0, lambda: messagebox.showerror("Error", err))
            finally:
                self.frame.after(
                    0,
                    lambda: self.run_btn.config(
                        state="normal", text="Generate GMB Keywords"
                    ),
                )

        threading.Thread(target=task, daemon=True).start()

    def show_help(self) -> None:
        """Display help dialog explaining the GMB Keyword Generator tool."""
        help_msg = (
            "WHAT THIS DOES:\n"
            "Generates Google Business Profile keyword variations for local SEO.\n"
            "Creates 4 variants per service:\n"
            "  1. [Business Name] [Service] [City]\n"
            "  2. [Service] near [City]\n"
            "  3. Best [Service] in [City]\n"
            "  4. [City] [Service]\n\n"
            "WHAT YOU NEED TO ENTER:\n"
            "1. Business Name - the client's company name\n"
            "2. Services - comma-separated list (e.g. AC repair, furnace install)\n"
            "3. City - client's city\n"
            "4. State - two-letter abbreviation (e.g. MI, OH, TX)\n"
            "5. Output Root Directory - folder where gmb_keywords.txt will be saved\n\n"
            "OUTPUT FILE:\n"
            "{Output Root}\\{Business Name}\\gmb_keywords.txt"
        )
        messagebox.showinfo("GMB Keyword Generator Help", help_msg)

    def get_frame(self) -> ttk.Frame:
        """Return the main frame widget for this tab.

        Returns:
            The ttk.Frame containing all tab UI elements.
        """
        return self.frame
