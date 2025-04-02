from faq_generator import run_faq_generator

client_config = {
    "name": "Tri-State Heating & Cooling, LLC",
    "city": "Adrian",
    "state": "MI",
    "seed_keyword": "HVAC contractor",
    "output_root": r"C:\Users\georg\OneDrive\RankRocket\Clients\Patrick Rombyer"
}

run_faq_generator(client_config)