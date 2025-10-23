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
v1.02

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.02 - Added type hints and Google-style docstrings
* v1.01 - Added standardized file header and ASCII-only output
* v1.00 - Initial release with basic keyword generation
"""

from typing import Dict, Any, List


def run(config: Dict[str, Any]) -> None:
    """Generate Google Business Profile keyword variations and save to file.

    Creates 4 keyword variations per service for local SEO optimization:
    1. [Business Name] [Service] [Location]
    2. [Service] near [Location]
    3. Best [Service] in [Location]
    4. [Location] [Service]

    Service names are normalized to title case and empty strings are filtered out.
    Output is written to gmb_keywords.txt in the configured output directory.

    Args:
        config: Configuration dictionary containing:
            - name (str): Business name
            - services (List[str]): List of service names
            - city (str): City name
            - state (str): State abbreviation
            - output_root (str, optional): Output directory path. Defaults to "."

    Returns:
        None. Prints the count of generated keywords to stdout.

    Example:
        >>> config = {
        ...     "name": "ACME HVAC",
        ...     "services": ["ac repair", "heating"],
        ...     "city": "Phoenix",
        ...     "state": "AZ",
        ...     "output_root": "./output"
        ... }
        >>> run(config)
        Generated 8 keywords.
    """
    business_name = config.get("name")
    services = config.get("services", [])
    location = config.get("city") + ", " + config.get("state")

    # FIXED: Handle services as plain names, not URLs
    service_names: List[str] = [s.strip().title() for s in services if s.strip()]

    keywords: List[str] = []
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
