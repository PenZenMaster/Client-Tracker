# logic.py
from chatgpt_background import run as run_background_summary
from gmb_keywords import run as run_gmb_keywords
from faq_generator import run_faq_generator

def run_background(config):
    run_background_summary(config)

def run_gmb(config):
    services = config.get("services", [])
    if not services:
        raise ValueError("No services provided. Please enter at least one service name.")
    config["services"] = [s.strip().title() for s in services if s.strip()]
    run_gmb_keywords(config)

def run_faq(config):
    run_faq_generator(config)

def run_all(config):
    run_background(config)
    run_gmb(config)
    run_faq(config)
