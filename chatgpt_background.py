# chatgpt_background.py

import os
import openai
from docx import Document

def run(client_config):
    client_name = client_config["name"]
    output_path = os.path.join(client_config["output_root"], client_name)
    os.makedirs(output_path, exist_ok=True)

    # Handle different input scenarios
    url = client_config.get("url", "").strip()
    gbp_url = client_config.get("gbp_url", "").strip()

    if url and gbp_url:
        target_info = f"Website: {url}\nGoogle Business Profile: {gbp_url}"
    elif url:
        target_info = f"Website: {url}"
    elif gbp_url:
        target_info = f"Google Business Profile: {gbp_url}"
    else:
        raise ValueError("Client config must include either a 'url', 'gbp_url', or both.")

    # Generate prompt
    prompt = (
        "Please review the following business information and provide:\n"
        "- A summary of services offered\n"
        "- Background information on the business\n\n"
        f"{target_info}"
    )

    print(f"Generating background summary for {client_name}...")

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an SEO assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7
    )

    summary = response["choices"][0]["message"]["content"]

    # Save to Word doc
    doc = Document()
    doc.add_heading(f"{client_name} – Background Information", 0)
    doc.add_paragraph(summary)
    doc.save(os.path.join(output_path, f"{client_name} background information.docx"))

    print(f"Saved background info to {output_path}")