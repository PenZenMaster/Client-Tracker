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

    base_output = client_config["output_root"]
    if not base_output.lower().endswith(client_name.lower()):
        output_path = os.path.join(base_output, client_name)
    else:
        output_path = base_output

    os.makedirs(output_path, exist_ok=True)

    prompt = f"""
You are a local SEO expert. Based on the business niche "{niche}" and the location "{city}, {state}", generate a list of 25 high-opportunity local SEO keywords.

Organize the keywords into the following categories:
1. Primary Keywords
2. Service-Based Keywords
3. Geo-Modified Keywords
4. Long-Tail Local Questions

Please use clearly labeled section headers, and present each keyword in bullet-point format.

This is for a business listed on Google Business Profile:
{cid_url}

Output in clean, readable plain text with section titles and bullet points. No preamble.
"""

    print(f"Generating GMB keywords for {client_name} in {city}, {state}...")

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