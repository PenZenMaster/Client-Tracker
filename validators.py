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
v1.02

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.02 - Added type hints and Google-style docstrings
* v1.01 - Added standardized file header and ASCII-only output
* v1.00 - Initial release with config validation
"""

from typing import Dict, Any


def validate_config(config: Dict[str, Any]) -> None:
    """Validate that all required configuration fields are present.

    Args:
        config: Dictionary containing client configuration parameters.

    Raises:
        KeyError: If any required fields are missing from the configuration.

    Example:
        >>> config = {"name": "Test", "city": "NYC", "state": "NY",
        ...           "seed_keyword": "SEO", "output_root": "./out", "niche": "tech"}
        >>> validate_config(config)  # No error
        >>> validate_config({"name": "Test"})  # Raises KeyError
    """
    required_fields = ["name", "city", "state", "seed_keyword", "output_root", "niche"]
    missing = [field for field in required_fields if not config.get(field)]
    if missing:
        raise KeyError(f"Missing required fields: {', '.join(missing)}")
