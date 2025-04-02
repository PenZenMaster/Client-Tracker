# ui.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import json
import subprocess
from config_handler import load_config, save_config
from logic import run_all, run_faq, run_gmb, run_background
from validators import validate_config
from logger import log_event, log_error
from city_utils import handle_city_inputs


class SkippyUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Skippy - Client Launcher")
        self.root.geometry("780x700")
        self.root.resizable(False, False)
        self.fields = {}
        self.setup_style()
        self.create_form()

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", padding=5)
        style.configure("TButton", padding=6)

    def create_form(self):
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.grid(row=0, column=0, sticky="nsew")

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
            ("services", "Services (comma-separated)"),
        ]

        for i, (key, label_text) in enumerate(self.field_names):
            label = ttk.Label(form_frame, text=label_text)
            label.grid(row=i, column=0, sticky="e", pady=4, padx=5)
            entry = ttk.Entry(form_frame, width=50)
            entry.grid(row=i, column=1, pady=4, padx=5)
            self.fields[key] = entry

        self.auto_city_var = tk.BooleanVar()
        self.auto_city_check = ttk.Checkbutton(
            form_frame,
            text="Auto-generate Nearby Cities",
            variable=self.auto_city_var
        )
        self.auto_city_check.grid(row=len(self.field_names), columnspan=2, pady=10)

        self.fields["nearby_10mi"] = ttk.Entry(form_frame, width=50)
        self.fields["nearby_20mi"] = ttk.Entry(form_frame, width=50)
        ttk.Label(form_frame, text="Nearby 10mi (comma-separated)").grid(row=len(self.field_names)+1, column=0, sticky="e", pady=4)
        self.fields["nearby_10mi"].grid(row=len(self.field_names)+1, column=1, pady=4)
        ttk.Label(form_frame, text="Nearby 20mi (comma-separated)").grid(row=len(self.field_names)+2, column=0, sticky="e", pady=4)
        self.fields["nearby_20mi"].grid(row=len(self.field_names)+2, column=1, pady=4)

        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.grid(row=1, column=0, pady=10)
        ttk.Button(button_frame, text="1. Load Existing Config", command=self.load_config).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="2. Run Background Summary", command=self.run_background).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="3. Run GMB Keywords", command=self.run_gmb).grid(row=1, column=0, padx=5)
        ttk.Button(button_frame, text="4. Run FAQ Generator", command=self.run_faq).grid(row=1, column=1, padx=5)
        ttk.Button(button_frame, text="5. Save Config", command=self.save_config).grid(row=2, column=0, padx=5)
        ttk.Button(button_frame, text="6. Run All", command=self.run_all).grid(row=2, column=1, padx=5)

    def get_config(self):
        config = {key: entry.get().strip() for key, entry in self.fields.items()}
        if not config.get("output_root"):
            config["output_root"] = os.getcwd()
        config["services"] = [s.strip() for s in config["services"].split(",") if s.strip()]
        config["nearby_10mi"] = [s.strip() for s in config["nearby_10mi"].split(",") if s.strip()]
        config["nearby_20mi"] = [s.strip() for s in config["nearby_20mi"].split(",") if s.strip()]
        if self.auto_city_var.get():
            config = handle_city_inputs(config)
        return config

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

    def run_background(self):
        self._safe_process(run_background, "Run Background Summary")

    def run_gmb(self):
        self._safe_process(run_gmb, "Run GMB Keywords")

    def run_faq(self):
        self._safe_process(run_faq, "Run FAQ Generator")

    def run_all(self):
        self._safe_process(run_all, "Run All")

    def _safe_process(self, func, label):
        try:
            config = self.get_config()
            validate_config(config)
            log_event(f"START: {label}")
            func(config)
            log_event(f"END: {label}")
            messagebox.showinfo("Success", f"{label} completed successfully!")
        except Exception as e:
            self.show_error(label, e)

    def show_error(self, label, error):
        log_error(label, error)
        response = messagebox.askyesno(
            title=f"{label} Error",
            message=f"An error occurred:\n{str(error)}\n\nOpen log file?"
        )
        if response:
            try:
                log_path = os.path.abspath("log.txt")
                os.startfile(log_path)
            except Exception as e:
                messagebox.showerror("Error Opening Log", str(e))


def launch_ui():
    root = tk.Tk()
    app = SkippyUI(root)
    root.mainloop()
