r"""
Module/Script Name: faq_generator_ui.py
Path: E:\projects\Project Tracking\faq_generator_ui.py

Description:
Tkinter UI tab for the FAQ Content Generator. Provides form inputs for client
configuration and triggers SerpAPI + GPT-4 FAQ generation workflow.

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
* v1.00 - Initial release with Tkinter UI tab for FAQTab
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox

from faq_generator import run_faq_generator


class FAQTab:
    """Tkinter tab interface for the FAQ Content Generator.

    Provides form inputs for:
    - Business name
    - City
    - State abbreviation
    - Seed keyword
    - Output root directory
    - Max questions (optional)

    Runs FAQ generation in a background thread so the GUI remains responsive
    during SerpAPI and OpenAI API calls.

    Attributes:
        frame: Main ttk.Frame container for the tab.
        name_entry: Entry field for business name.
        city_entry: Entry field for city name.
        state_entry: Entry field for state abbreviation.
        keyword_entry: Entry field for seed keyword.
        output_root_entry: Entry field for output directory path.
        max_questions_entry: Entry field for max question count.
        run_btn: Button to trigger FAQ generation.
    """

    def __init__(self, parent: tk.Widget) -> None:
        """Initialize the FAQ Generator tab.

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

        ttk.Label(self.frame, text="City:").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.city_entry = ttk.Entry(self.frame, width=40)
        self.city_entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="State (abbreviation):").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.state_entry = ttk.Entry(self.frame, width=10)
        self.state_entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="Seed Keyword:").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.keyword_entry = ttk.Entry(self.frame, width=60)
        self.keyword_entry.insert(0, "HVAC contractor")
        self.keyword_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="Output Root Directory:").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.output_root_entry = ttk.Entry(self.frame, width=60)
        self.output_root_entry.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        ttk.Label(self.frame, text="Max Questions (default 20):").grid(
            row=row, column=0, sticky="e", pady=5, padx=5
        )
        self.max_questions_entry = ttk.Entry(self.frame, width=10)
        self.max_questions_entry.insert(0, "20")
        self.max_questions_entry.grid(row=row, column=1, sticky="w", pady=5, padx=5)
        row += 1

        self.run_btn = ttk.Button(
            self.frame, text="Generate FAQs", command=self.run_faq
        )
        self.run_btn.grid(row=row, column=0, columnspan=2, pady=10)
        row += 1

        ttk.Button(self.frame, text="Help", command=self.show_help).grid(
            row=row, column=0, columnspan=2
        )

    def run_faq(self) -> None:
        """Validate inputs and launch FAQ generation in a thread.

        Disables the run button during execution to prevent duplicate runs.
        Shows a completion or error dialog when finished.
        """
        name = self.name_entry.get().strip()
        city = self.city_entry.get().strip()
        state = self.state_entry.get().strip()
        seed_keyword = self.keyword_entry.get().strip()
        output_root = self.output_root_entry.get().strip()
        max_questions_raw = self.max_questions_entry.get().strip()

        if not all([name, city, state, seed_keyword, output_root]):
            messagebox.showerror(
                "Missing Fields",
                "Business Name, City, State, Seed Keyword, and Output Root are all required.",
            )
            return

        try:
            max_questions = int(max_questions_raw) if max_questions_raw else 20
        except ValueError:
            messagebox.showerror("Invalid Input", "Max Questions must be a number.")
            return

        client_config = {
            "name": name,
            "city": city,
            "state": state,
            "seed_keyword": seed_keyword,
            "output_root": output_root,
            "max_questions": max_questions,
        }

        self.run_btn.config(state="disabled", text="Generating FAQs...")

        def task() -> None:
            try:
                run_faq_generator(client_config)
                self.frame.after(
                    0,
                    lambda: messagebox.showinfo(
                        "Complete",
                        f"FAQ HTML saved to:\n{output_root}\\{name}\\G Site\\",
                    ),
                )
            except Exception as exc:
                err = str(exc)
                self.frame.after(0, lambda: messagebox.showerror("Error", err))
            finally:
                self.frame.after(
                    0,
                    lambda: self.run_btn.config(state="normal", text="Generate FAQs"),
                )

        threading.Thread(target=task, daemon=True).start()

    def show_help(self) -> None:
        """Display help dialog explaining the FAQ Generator tool."""
        help_msg = (
            "WHAT THIS DOES:\n"
            "Fetches 'People Also Ask' questions from Google via SerpAPI for your\n"
            "seed keyword, then uses GPT-4 to write professional answers. Outputs\n"
            "an HTML accordion file ready to embed on a website.\n\n"
            "WHAT YOU NEED TO ENTER:\n"
            "1. Business Name - the client's company name\n"
            "2. City - client's city\n"
            "3. State - two-letter abbreviation (e.g. MI, OH, TX)\n"
            "4. Seed Keyword - the topic to research (e.g. 'HVAC contractor')\n"
            "5. Output Root Directory - folder where the HTML will be saved\n"
            "6. Max Questions - how many Q&A pairs to generate (default: 20)\n\n"
            "OUTPUT FILE:\n"
            "{Output Root}\\{Business Name}\\G Site\\{Business Name} - FAQs.html\n\n"
            "REQUIREMENTS:\n"
            "- OPENAI_API_KEY must be set in your .env file\n"
            "- SERPAPI_KEY must be set in your .env file"
        )
        messagebox.showinfo("FAQ Generator Help", help_msg)

    def get_frame(self) -> ttk.Frame:
        """Return the main frame widget for this tab.

        Returns:
            The ttk.Frame containing all tab UI elements.
        """
        return self.frame
