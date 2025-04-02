# city_utils.py

def handle_city_inputs(config):
    base_city = config.get("city", "")
    # Dummy logic - replace with actual radius-based lookup if needed
    generated_10mi = [base_city + " Heights", base_city + " North"]
    generated_20mi = [base_city + " Valley", base_city + " Junction"]

    config["nearby_10mi"] = generated_10mi
    config["nearby_20mi"] = generated_20mi
    return config
