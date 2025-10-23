r"""
Module/Script Name: logic.py
Path: E:\projects\Project Tracking\logic.py

Description:
Central business logic controller for SEO automation workflows. Orchestrates execution
of background summaries, GMB keywords, and FAQ generation modules.

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
* v1.00 - Initial release with workflow orchestration
"""

from typing import Dict, Any
from chatgpt_background import run as run_background_summary
from gmb_keywords import run as run_gmb_keywords
from faq_generator import run_faq_generator


def run_background(config: Dict[str, Any]) -> None:
    """Execute business background summary generation workflow.

    Args:
        config: Client configuration dictionary with business details.
    """
    run_background_summary(config)


def run_gmb(config: Dict[str, Any]) -> None:
    """Execute Google Business Profile keyword generation workflow.

    Validates that services are provided, normalizes service names,
    and generates GBP keyword variations.

    Args:
        config: Client configuration dictionary with services list.

    Raises:
        ValueError: If no services are provided in configuration.

    Example:
        >>> config = {"services": ["hvac repair", "ac installation"]}
        >>> run_gmb(config)
    """
    services = config.get("services", [])
    if not services:
        raise ValueError(
            "No services provided. Please enter at least one service name."
        )
    config["services"] = [s.strip().title() for s in services if s.strip()]
    run_gmb_keywords(config)


def run_faq(config: Dict[str, Any]) -> None:
    """Execute FAQ content generation workflow.

    Args:
        config: Client configuration dictionary with seed keyword.
    """
    run_faq_generator(config)


def run_all(config: Dict[str, Any]) -> None:
    """Execute all SEO content generation workflows in sequence.

    Runs background summary, GMB keywords, and FAQ generation.

    Args:
        config: Client configuration dictionary with all required fields.

    Example:
        >>> config = {"name": "HVAC Co", "services": ["repair"], "seed_keyword": "HVAC"}
        >>> run_all(config)
    """
    run_background(config)
    run_gmb(config)
    run_faq(config)
