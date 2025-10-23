r"""
Module/Script Name: run_chatgpt_background.py
Path: E:\projects\Project Tracking\run_chatgpt_background.py

Description:
Runner script for business background summary generator. Example client configuration
for GPT-4 based business background content generation.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2024-01-15

Last Modified Date:
2025-10-23

Version:
v1.02

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.02 - Added type hints for config dictionary
* v1.01 - Added standardized file header
* v1.00 - Initial release with example client config
"""

from typing import Dict, Any
from chatgpt_background import run

# Example client configuration for business background generation
client_config: Dict[str, Any] = {
    "name": "Tri-State Heating & Cooling, LLC",
    "address": "7686 Rome Rd, Adrian, MI 49221",
    "url": "https://www.tri-stateheating.com/",
    "mobile_url": "https://www.tristate-hvac.com/",
    "gbp_url": "https://g.co/kgs/j3Bb4gy",
    "output_root": r"C:\Users\georg\OneDrive\RankRocket\Clients\Patrick Rombyer",
}

run(client_config)
