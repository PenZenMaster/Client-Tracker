r"""
Module/Script Name: gmb_keywords.py
Path: E:\projects\Project Tracking\gmb_keywords.py

Description:
Generates Google Business Profile (GBP) keyword combinations based on business
name, services, and location. Creates local SEO keyword variations for GMB optimization.

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
* v1.01 - Added standardized file header and ASCII-only output
* v1.00 - Initial release with basic keyword generation
"""


def run(config):
    business_name = config.get("name")
    services = config.get("services", [])
    location = config.get("city") + ", " + config.get("state")

    # FIXED: Handle services as plain names, not URLs
    service_names = [s.strip().title() for s in services if s.strip()]

    keywords = []
    for service in service_names:
        keywords.append(f"{business_name} {service} {location}")
        keywords.append(f"{service} near {location}")
        keywords.append(f"Best {service} in {location}")
        keywords.append(f"{location} {service}")

    output_file = config.get("output_root", ".") + "/gmb_keywords.txt"
    with open(output_file, "w", encoding="utf-8") as f:
        for kw in keywords:
            f.write(kw + "\n")

    print(f"Generated {len(keywords)} keywords.")
