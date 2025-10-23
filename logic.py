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
v1.01

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.01 - Added standardized file header and ASCII-only output
* v1.00 - Initial release with workflow orchestration
"""

from chatgpt_background import run as run_background_summary
from gmb_keywords import run as run_gmb_keywords
from faq_generator import run_faq_generator


def run_background(config):
    run_background_summary(config)


def run_gmb(config):
    services = config.get("services", [])
    if not services:
        raise ValueError(
            "No services provided. Please enter at least one service name."
        )
    config["services"] = [s.strip().title() for s in services if s.strip()]
    run_gmb_keywords(config)


def run_faq(config):
    run_faq_generator(config)


def run_all(config):
    run_background(config)
    run_gmb(config)
    run_faq(config)
