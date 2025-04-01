import os
from openai import OpenAI
from dotenv import load_dotenv
from docx import Document

# Load API Key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def run(client_config):
    client_name = client_config["name"]
    output_path = os.path.join(client_config["output_root"], client_name)
    os.makedirs(output_path, exist_ok=True)

    url = client_config.get("url", "").strip()
    mobile_url = client_config.get("mobile_url", "").strip()
    gbp_url = client_config.get("gbp_url", "").strip()
    address = client_config.get("address", "Unknown")

    prompt = (
        f"I am gathering background information about the following local HVAC company. "
        f"Please summarize the services they offer and provide any business background information based on the name, address, and URLs provided:\n\n"
        f"Business Name: {client_name}\n"
        f"Address: {address}\n"
        f"Website: {url}\n"
        f"Mobile Site: {mobile_url}\n"
        f"Google Business Profile: {gbp_url}"
    )

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
    output_file = os.path.join(output_path, f"{client_name} background information.docx")
    doc.save(output_file)

    print(f"Saved background info to {output_file}")
