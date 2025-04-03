# Author: Skippy the Magnificent along with that dumb ape, George Penzenik
# Version: 1.14
# Date Modified: 18:25 04/02/2025
# Comment:
#  - Full manual rewrite to eliminate indentation errors and stabilize layout
#  - Includes splash overlay text, horizontal buttons, help dialog, and proper scrolling

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import os
import json
from config_handler import load_config, save_config
from logic import run_all, run_faq, run_gmb, run_background
from validators import validate_config
from logger import log_event, log_error
from city_utils import handle_city_inputs

APP_VERSION = "1.14"

HELP_TEXT = """🧠 PURPOSE:
This app helps generate background summaries, branded GMB keywords, and SEO-rich FAQs.

🛠 REQUIRED FIELDS:
- Business Name
- City, State
- Seed Keyword
- Niche
- Output Directory

📜 LICENSE:
Creative Commons Attribution-ShareAlike 4.0 International
https://creativecommons.org/licenses/by-sa/4.0/
"""

class SkippyUI:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Skippy - Client Launcher v{APP_VERSION}")
        self.root.geometry("800x750")
        self.root.resizable(False, False)
        self.fields = {}
        self.setup_scrollable_form()

    def setup_scrollable_form(self):
        canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.build_form(scroll_frame)

    def build_form(self, container):
        self.field_names = [
            ("name", "* Business Name"),
            ("city", "* City"),
            ("state", "* State"),
            ("seed_keyword", "* Seed Keyword"),
            ("output_root", "* Output Directory"),
            ("niche", "* Niche"),
            ("gbp_url", "GBP URL"),
            ("address", "Business Address"),
            ("url", "Website URL"),
            ("mobile_url", "Mobile Website URL"),
            ("services", "Services (comma-separated)")
        ]

        for i, (key, label) in enumerate(self.field_names):
            ttk.Label(container, text=label).grid(row=i, column=0, sticky="e", pady=4, padx=5)
            entry = ttk.Entry(container, width=50)
            entry.grid(row=i, column=1, pady=4, padx=5)
            self.fields[key] = entry

        self.auto_city_var = tk.BooleanVar()
        ttk.Checkbutton(container, text="Auto-generate Nearby Cities", variable=self.auto_city_var).grid(
            row=len(self.field_names), columnspan=2, pady=10)

        self.fields["nearby_10mi"] = ttk.Entry(container, width=50)
        self.fields["nearby_20mi"] = ttk.Entry(container, width=50)
        ttk.Label(container, text="Nearby 10mi (comma-separated)").grid(row=len(self.field_names)+1, column=0, sticky="e", pady=4)
        self.fields["nearby_10mi"].grid(row=len(self.field_names)+1, column=1, pady=4)
        ttk.Label(container, text="Nearby 20mi (comma-separated)").grid(row=len(self.field_names)+2, column=0, sticky="e", pady=4)
        self.fields["nearby_20mi"].grid(row=len(self.field_names)+2, column=1, pady=4)

        row_offset = len(self.field_names) + 3
        btn_row = ttk.Frame(container)
        btn_row.grid(row=row_offset, column=0, columnspan=2, pady=10)

        button_defs = [
            ("1. Load Config", self.load_config),
            ("2. Run Background", lambda: self.run_task(run_background, "Background Summary")),
            ("3. Run GMB Keywords", lambda: self.run_task(run_gmb, "GMB Keywords")),
            ("4. Run FAQ Generator", lambda: self.run_task(run_faq, "FAQ Generator")),
            ("5. Save Config", self.save_config),
            ("6. Run All", lambda: self.run_task(run_all, "Run All Tasks")),
            ("Help", self.show_help)
        ]

        for i, (text, command) in enumerate(button_defs):
            ttk.Button(btn_row, text=text, command=command).grid(row=0, column=i, padx=5, pady=4)

    def get_config(self):
        config = {key: entry.get().strip() for key, entry in self.fields.items()}
        config["services"] = [s.strip() for s in config["services"].split(",") if s.strip()]
        config["nearby_10mi"] = [s.strip() for s in config["nearby_10mi"].split(",") if s.strip()]
        config["nearby_20mi"] = [s.strip() for s in config["nearby_20mi"].split(",") if s.strip()]
        if not config.get("output_root"):
            config["output_root"] = os.getcwd()
        if self.auto_city_var.get():
            config = handle_city_inputs(config)
        return config

    def run_task(self, func, label):
        try:
            config = self.get_config()
            validate_config(config)
            log_event(f"START: {label}")
            func(config)
            log_event(f"END: {label}")
            messagebox.showinfo("Task Complete", f"{label} completed.\nOutput saved to:\n{config['output_root']}")
        except Exception as e:
            self.show_error(label, e)

    def save_config(self):
        try:
            config = self.get_config()
            save_config(config)
            messagebox.showinfo("Success", "Configuration saved successfully!")
        except Exception as e:
            self.show_error("Save Config", e)

    def load_config(self):
        try:
            filepath = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
            if filepath:
                config = load_config(filepath)
                for key, value in config.items():
                    if key in self.fields:
                        self.fields[key].delete(0, tk.END)
                        self.fields[key].insert(0, ", ".join(value) if isinstance(value, list) else str(value))
        except Exception as e:
            self.show_error("Load Config", e)

    def show_help(self):
        messagebox.showinfo("Skippy Help", HELP_TEXT)

    def show_error(self, label, error):
        log_error(label, error)
        response = messagebox.askyesno(
            title=f"{label} Error",
            message=f"An error occurred:\n{str(error)}\n\nOpen log file?"
        )
        if response:
            try:
                os.startfile(os.path.abspath("log.txt"))
            except Exception as e:
                messagebox.showerror("Error Opening Log", str(e))


def show_splash():
    splash = tk.Tk()
    splash.title("Launching Skippy...")
    splash.update_idletasks()
    width, height = 640, 360
    x = (splash.winfo_screenwidth() // 2) - (width // 2)
    y = (splash.winfo_screenheight() // 2) - (height // 2)
    splash.geometry(f"{width}x{height}+{x}+{y}")
    splash.overrideredirect(True)

    try:
        image = Image.open("skippy_the_magnificient.jpg")
        splash_img = ImageTk.PhotoImage(image.resize((640, 360)))
        canvas = tk.Canvas(splash, width=640, height=360)
        canvas.pack()
        canvas.create_image(0, 0, anchor="nw", image=splash_img)
        canvas.image = splash_img
        
    except:
        label = tk.Label(splash, text="This software is brought to you by Skippy the Magnificent\nand unfortunately with some insy weensy help from a meat sack named George Penzenik.",
                         font=("Segoe UI", 12), padx=20, pady=40)
        label.pack()

    splash.after(3000, splash.destroy)
    splash.mainloop()

def launch_ui():
    show_splash()
    root = tk.Tk()
    w, h = 800, 750
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")
    app = SkippyUI(root)
    root.mainloop()
