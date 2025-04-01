from gmb_keywords import run

client_config = {
    "name": "Tri-State Heating & Cooling, LLC",
    "niche": "HVAC",
    "city": "Adrian",
    "state": "MI",
    "gbp_url": "https://www.google.com/maps?cid=3560100286428651288",
    "output_root": r"C:\Users\georg\OneDrive\RankRocket\Clients\Patrick Rombyer",
    "services": [
        "https://www.tri-stateheating.com/services/commercial-hvac-services/",
        "https://www.tri-stateheating.com/services/hvac-installers/",
        "https://www.tri-stateheating.com/services/hvac-maintenance-services/",
        "https://www.tri-stateheating.com/services/residential-hvac-services/"
    ],
    "nearby_10mi": ["Tecumseh", "Blissfield"],
    "nearby_20mi": ["Toledo", "Wauseon", "Jackson", "Brighton", "Ypsilanti"]
}

run(client_config)