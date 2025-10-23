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
2025-10-23

Version:
v1.01

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.01 - Added standardized file header
* v1.00 - Initial release with example client config
"""

from gmb_keywords import run

client_config = {
    "name": "Tri-State Heating & Cooling, LLC",
    "niche": "HVAC",
    "city": "Adrian",
    "state": "MI",
    "gbp_url": "https://www.google.com/maps?cid=3560100286428651288",
    "output_root": r"C:\Users\georg\OneDrive\RankRocket\Clients\Patrick Rombyer",
    "services": [
        "https://www.tri-stateheating.com/services/commercial-hvac-services/",
        "https://www.tri-stateheating.com/services/hvac-installers/",
        "https://www.tri-stateheating.com/services/hvac-maintenance-services/",
        "https://www.tri-stateheating.com/services/residential-hvac-services/",
    ],
    "nearby_10mi": ["Tecumseh", "Blissfield"],
    "nearby_20mi": ["Toledo", "Wauseon", "Jackson", "Brighton", "Ypsilanti"],
}

run(client_config)
