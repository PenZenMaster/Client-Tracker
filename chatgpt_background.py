import os
from openai import OpenAI
from dotenv import load_dotenv
from docx import Document
from scraper import scrape_website_text

# Load API Key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def run(client_config):
    client_name = client_config["name"]
    address = client_config.get("address", "Unknown")
    url = client_config.get("url", "").strip()
    mobile_url = client_config.get("mobile_url", "").strip()
    gbp_url = client_config.get("gbp_url", "").strip()
    base_output = client_config["output_root"]

    if not base_output.lower().endswith(client_name.lower()):
        output_path = os.path.join(base_output, client_name)
    else:
        output_path = base_output

    os.makedirs(output_path, exist_ok=True)

    # Scrape site content
    site_text = scrape_website_text(url)

    # Use triple quotes to avoid escape hell
    prompt = f"""Based on the following website content, provide a summary of services
and background information for this HVAC company.

Business Name: {client_name}
Address: {address}
Website Content:
{site_text}
"""

    print(f"Generating background summary for {client_name}...")

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an SEO assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    summary = response.choices[0].message.content

    doc = Document()
    doc.add_heading(f"{client_name} – Background Information", 0)
    doc.add_paragraph(summary)
    output_file = os.path.join(
        output_path, f"{client_name} background information.docx"
    )
    doc.save(output_file)

    print(f"Saved background info to {output_file}")
