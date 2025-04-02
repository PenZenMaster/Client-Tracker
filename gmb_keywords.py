# gmb_keywords.py

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
