# validators.py

def validate_config(config):
    required_fields = ["name", "city", "state", "seed_keyword", "output_root", "niche"]
    missing = [field for field in required_fields if not config.get(field)]
    if missing:
        raise KeyError(f"Missing required fields: {', '.join(missing)}")
