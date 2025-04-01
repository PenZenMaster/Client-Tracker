import os
from openai import OpenAI
from dotenv import load_dotenv

# Load OpenAI API Key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run(client_config):
    client_name = client_config["name"]
    city = client_config["city"]
    state = client_config["state"]
    niche = client_config["niche"]
    cid_url = client_config.get("gbp_url", "")
    services = client_config.get("services", [])
    towns_10mi = client_config.get("nearby_10mi", [])
    towns_20mi = client_config.get("nearby_20mi", [])

    base_output = client_config["output_root"]
    if not base_output.lower().endswith(client_name.lower()):
        output_path = os.path.join(base_output, client_name)
    else:
        output_path = base_output

    os.makedirs(output_path, exist_ok=True)

    # Build service summary string
    service_names = [s.split("/")[-2].replace("-", " ").title() for s in services]
    service_summary = ", ".join(service_names)

    prompt = f"""
You are an advanced local SEO assistant.

The business name is: {client_name}
Niche: {niche}
Primary Location: {city}, {state}
Service Types: {service_summary}
Google Business Profile: {cid_url}

Generate a list of branded local SEO keywords that answer:
1. Who are you?
2. What do you do?
3. Where do you do it?

Group the branded keywords by geography as follows:

**Branded Keywords – Primary Location ({city}, {state})**

Generate keywords that include the business name, services, and location.

**Branded Keywords – Within 10 Miles**
Cities: {", ".join(towns_10mi)}

**Branded Keywords – Within 20 Miles**
Cities: {", ".join(towns_20mi)}

Each group should include keywords using the format:
- Business name + service + city + state

Present everything in clean bullet-point format with clear headers. Skip preambles, explanations, or conclusions.
"""

    print(f"Generating Branded Keywords for {client_name}...")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a local SEO keyword research assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    keyword_output = response.choices[0].message.content

    out_path = os.path.join(output_path, "GMB Keywords.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(keyword_output)

    print(f"Saved GMB keyword suggestions to {out_path}")