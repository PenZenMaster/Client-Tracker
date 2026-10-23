r"""
Module/Script Name: run_gmb_keywords.py
Path: E:\projects\Project Tracking\run_gmb_keywords.py

Description:
Runner script for GMB keyword generator. Example client configuration for
Tri-State Heating & Cooling HVAC business keyword generation.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2024-01-15

Last Modified Date:
2026-10-23

Version:
v1.04

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.04 - Derive output_root from Path.home() (client folder renamed to patrick_rombyer)
* v1.02 - Added type hints for config dictionary
* v1.01 - Added standardized file header
* v1.00 - Initial release with example client config
"""

from pathlib import Path
from typing import Dict, Any
from gmb_keywords import run

# Example client configuration for GMB keyword generation
client_config: Dict[str, Any] = {
    "name": "Tri-State Heating & Cooling, LLC",
    "niche": "HVAC",
    "city": "Adrian",
    "state": "MI",
    "gbp_url": "https://www.google.com/maps?cid=3560100286428651288",
    "output_root": str(
        Path.home() / "OneDrive" / "RankRocket" / "Clients" / "patrick_rombyer"
    ),
    "services": [
        "https://www.tri-stateheating.com/services/commercial-hvac-services/",
        "https://www.tri-stateheating.com/services/hvac-installers/",
        "https://www.tri-stateheating.com/services/hvac-maintenance-services/",
        "https://www.tri-stateheating.com/services/residential-hvac-services/",
    ],
    "nearby_10mi": ["Tecumseh", "Blissfield"],
    "nearby_20mi": ["Toledo", "Wauseon", "Jackson", "Brighton", "Ypsilanti"],
}

if __name__ == "__main__":
    run(client_config)
