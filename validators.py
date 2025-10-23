r"""
Module/Script Name: validators.py
Path: E:\projects\Project Tracking\validators.py

Description:
Configuration validation utilities for SEO automation toolkit. Ensures required
fields are present before executing workflows.

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
* v1.00 - Initial release with config validation
"""


def validate_config(config):
    required_fields = ["name", "city", "state", "seed_keyword", "output_root", "niche"]
    missing = [field for field in required_fields if not config.get(field)]
    if missing:
        raise KeyError(f"Missing required fields: {', '.join(missing)}")
