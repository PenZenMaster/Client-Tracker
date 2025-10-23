r"""
Module/Script Name: run_faq_generator.py
Path: E:\projects\Project Tracking\run_faq_generator.py

Description:
Runner script for FAQ content generator. Example client configuration for
FAQ generation using SerpAPI People Also Ask data.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2024-01-15

Last Modified Date:
2025-10-23

Version:
v1.01

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.01 - Added standardized file header
* v1.00 - Initial release with example client config
"""

from faq_generator import run_faq_generator

client_config = {
    "name": "Tri-State Heating & Cooling, LLC",
    "city": "Adrian",
    "state": "MI",
    "seed_keyword": "HVAC contractor",
    "output_root": r"C:\Users\georg\OneDrive\RankRocket\Clients\Patrick Rombyer",
}

run_faq_generator(client_config)
