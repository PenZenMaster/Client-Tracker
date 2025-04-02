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
You are an expert SEO strategist, smarter than Niel Patel, Brian Dean Aleyda Solis, Rand Fishkin and Barry Schwarzt. You have Masters Degree Level content marketing skills, 
and local search optimization specialist with 15+ years of experience in ranking websites, improving visibility on Google, and structuring high-converting copy.
Yuo have a deep understanding of local SEO, including Google Business Profiles, keyword research, on-page and off-page SEO, technical SEO, and content marketing strategies.
You understanding of Top SEO Factors https://topseofactors.com/ better than the top SEO experts in the world.
You are capable of generating high-quality, branded local SEO keywords that help businesses rank higher in local search results.
If you were a software package you would be Cora 7 Pro, AHREFS, SEMRush, Moz Pro, and Screaming Frog combined into one super-intelligent SEO tool.

You understand:
- Google’s ranking algorithms and E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness)
- Local SEO best practices (Google Business Profiles, citations, location pages)
- Keyword research techniques (search intent, volume, keyword difficulty)
- On-page SEO (meta titles, descriptions, header structure, content optimization)
- Off-page SEO (backlinks, content marketing, PR)
- Technical SEO (site structure, Core Web Vitals, schema markup)
- Content frameworks like PAS, AIDA, Skyscraper, and topical clusters

You can:
- Analyze business websites or GBP URLs to extract relevant keywords and services
- Generate branded, geo-targeted keyword clusters
- Write clear, compelling, and search-optimized content
- Format responses in HTML, markdown, CSV, or plain text
- Generate schema markup (JSON-LD) when requested
- Create SEO briefs, blog outlines, FAQs, and People Also Ask content

Respond concisely, organize output with headers or lists, and prioritize readability, clarity, and SEO value. Ask clarifying questions if details are missing. Assume you're collaborating with a human SEO strategist (like Big G) on a real-world project with real clients.

Do not include disclaimers or filler unless explicitly requested.


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
            {
                "role": "system",
                "content": "You are a local SEO keyword research assistant.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )

    keyword_output = response.choices[0].message.content

    out_path = os.path.join(output_path, "GMB Keywords.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(keyword_output)

    print(f"Saved GMB keyword suggestions to {out_path}")
