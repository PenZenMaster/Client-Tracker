r"""
Module/Script Name: faq_generator.py
Path: E:\projects\Project Tracking\faq_generator.py

Description:
FAQ content generator using SerpAPI for "People Also Ask" questions and OpenAI
GPT-4 for answer drafting. Exports FAQ content to DOCX format.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2025-04-03

Last Modified Date:
2025-10-23

Version:
v1.06

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.06 - Added type hints and Google-style docstrings
* v1.05 - Added standardized file header, removed emojis (Windows compat)
* v1.04 - Removed broken location param from final SerpAPI query
* v1.04 - Fully relies on resolved uule for geo-targeting
"""

import os
from typing import Dict, Any, List, Tuple, Optional
import requests  # type: ignore[import-untyped]
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def resolve_uule(geo_target: str) -> Optional[str]:
    """Resolve geographic location to Google UULE (Unique User Location Encoding).

    Args:
        geo_target: Location string (e.g., "Adrian, MI", "Phoenix, AZ").

    Returns:
        UULE code string for SerpAPI geo-targeting, or None if resolution fails.

    Example:
        >>> resolve_uule("Phoenix, AZ")
        'w+CAIQICI...'
    """
    print(f"[INFO] Resolving uule for: {geo_target}")
    try:
        loc_params = {"q": geo_target, "limit": 1, "api_key": SERPAPI_KEY}
        res = requests.get("https://serpapi.com/locations.json", params=loc_params)
        data = res.json()
        if data and isinstance(data, list) and "uule" in data[0]:
            print(f"[SUCCESS] uule found: {data[0]['uule']}")
            return data[0]["uule"]
        else:
            print("[WARNING] uule not found, defaulting to no geo-targeting")
            return None
    except Exception as e:
        print("[ERROR] Error resolving uule:", e)
        return None


def fetch_paa_questions(
    seed_keyword: str,
    location: str = "us",
    max_questions: int = 20,
    geo_target: str = "Adrian, MI",
) -> List[str]:
    """Fetch 'People Also Ask' questions from Google search results via SerpAPI.

    Queries multiple keyword variants and pagination to collect unique questions
    from Google's "People Also Ask" feature for SEO FAQ content generation.

    Args:
        seed_keyword: Primary keyword to base question research on.
        location: Two-letter country code for search region. Defaults to "us".
        max_questions: Maximum number of unique questions to collect. Defaults to 20.
        geo_target: City/state for local geo-targeting (e.g., "Adrian, MI").

    Returns:
        List of unique question strings from PAA results, limited to max_questions.

    Example:
        >>> questions = fetch_paa_questions("hvac repair", geo_target="Phoenix, AZ")
        >>> print(len(questions))
        20
        >>> print(questions[0])
        'How much does HVAC repair cost?'
    """
    print(f"Starting PAA fetch for seed: {seed_keyword}")
    uule_code = resolve_uule(geo_target)

    keyword_variants = [
        seed_keyword,
        f"{seed_keyword} near me",
        f"{seed_keyword} {geo_target}",
        f"common questions about {seed_keyword}",
        f"{seed_keyword} services",
        f"what to know about {seed_keyword}",
    ]

    questions: List[str] = []
    seen: set[str] = set()

    for kw in keyword_variants:
        for start in [0, 10, 20]:
            if len(questions) >= max_questions:
                break

            print(f"Fetching for variant: {kw} (start={start})")
            params = {
                "engine": "google",
                "q": kw,
                "hl": "en",
                "gl": location,
                "start": start,
                "api_key": SERPAPI_KEY,
            }
            if uule_code:
                params["uule"] = uule_code

            res = requests.get("https://serpapi.com/search", params=params)
            print("SerpAPI status code:", res.status_code)

            try:
                data = res.json()
            except Exception as e:
                print("Error decoding SerpAPI response:", e)
                continue

            if "error" in data:
                print("SerpAPI error:", data["error"])
                continue

            if "related_questions" in data:
                print(f"→ {len(data['related_questions'])} results found for variant")
                for q in data["related_questions"]:
                    question = q.get("question")
                    if question and question not in seen:
                        questions.append(question)
                        seen.add(question)
                    if len(questions) >= max_questions:
                        break

    print(f"✅ Returning {len(questions)} unique questions.")
    return questions[:max_questions]


def generate_answer(question: str, business_name: str, city: str, state: str) -> str:
    """Generate SEO-optimized answer to a question using OpenAI GPT-4.

    Creates conversational, locally-targeted answers as if from the business perspective.

    Args:
        question: Question text to answer (typically from PAA results).
        business_name: Name of the business to answer as.
        city: City where business is located.
        state: State where business is located.

    Returns:
        Generated answer text as a string.

    Example:
        >>> answer = generate_answer(
        ...     "How much does HVAC repair cost?",
        ...     "ABC Heating",
        ...     "Phoenix",
        ...     "AZ"
        ... )
        >>> print(answer[:50])
        'HVAC repair costs can vary depending on the type...'
    """
    prompt = f"""Answer the following question as if you are an HVAC contractor named {business_name}, based in {city}, {state}:

Q: {question}

A:"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful, local HVAC expert providing SEO-optimized, conversational answers.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
    )
    content = response.choices[0].message.content
    return content.strip() if content else ""


def write_html_accordion(
    faq_list: List[Tuple[str, str]], business_name: str, output_path: str
) -> None:
    """Write FAQ question/answer pairs to an HTML accordion file.

    Generates an interactive HTML page with collapsible FAQ sections using
    vanilla JavaScript. Output styled with inline CSS for portability.

    Args:
        faq_list: List of (question, answer) tuples.
        business_name: Business name for page title and heading.
        output_path: Full file path where HTML should be saved.

    Returns:
        None. Writes HTML file to disk.

    Example:
        >>> faq_list = [("What is HVAC?", "HVAC stands for...")]
        >>> write_html_accordion(faq_list, "ABC Heating", "./output/faq.html")
    """
    html = f"""<!DOCTYPE html>
<html lang=\"en\">
<head>
    <meta charset=\"UTF-8\">
    <title>{business_name} - FAQs</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f9f9f9; padding: 20px; }}
        .accordion {{ background-color: #fff; border-radius: 10px; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .accordion-item {{ margin-bottom: 10px; }}
        .accordion-header {{ background-color: #eee; cursor: pointer; padding: 10px; border-radius: 6px; transition: 0.3s; }}
        .accordion-header:hover {{ background-color: #ddd; }}
        .accordion-content {{ display: none; padding: 10px; margin-top: 5px; }}
    </style>
</head>
<body>
    <h1>{business_name} - People Also Ask</h1>
    <div class=\"accordion\">
"""
    for i, (q, a) in enumerate(faq_list):
        html += f"""
        <div class=\"accordion-item\">
            <div class=\"accordion-header\" onclick=\"toggleContent('content{i}')\">{q}</div>
            <div class=\"accordion-content\" id=\"content{i}\">{a}</div>
        </div>
"""
    html += """
    </div>
    <script>
        function toggleContent(id) {
            var x = document.getElementById(id);
            x.style.display = (x.style.display === "block") ? "none" : "block";
        }
    </script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def run_faq_generator(client_config: Dict[str, Any]) -> None:
    """Execute complete FAQ generation workflow for a client.

    Main orchestration function that:
    1. Fetches PAA questions from Google via SerpAPI
    2. Generates answers using OpenAI GPT-4
    3. Writes HTML accordion file with all Q&A pairs

    Args:
        client_config: Configuration dictionary containing:
            - name (str): Business name
            - city (str): City name
            - state (str): State abbreviation
            - seed_keyword (str): Primary keyword for question research
            - output_root (str): Base output directory path
            - max_questions (int, optional): Max questions to generate. Defaults to 20.

    Returns:
        None. Writes HTML file to: {output_root}/{name}/G Site/{name} - FAQs.html

    Example:
        >>> config = {
        ...     "name": "ABC Heating",
        ...     "city": "Phoenix",
        ...     "state": "AZ",
        ...     "seed_keyword": "hvac repair",
        ...     "output_root": "./output",
        ...     "max_questions": 15
        ... }
        >>> run_faq_generator(config)
        [INFO] Saved FAQ HTML to: ./output/ABC Heating/G Site/ABC Heating - FAQs.html
    """
    business_name = client_config["name"]
    city = client_config["city"]
    state = client_config["state"]
    keyword = client_config["seed_keyword"]
    output_root = client_config["output_root"]
    max_questions = client_config.get("max_questions", 20)

    output_dir = os.path.join(output_root, business_name, "G Site")
    os.makedirs(output_dir, exist_ok=True)

    questions = fetch_paa_questions(
        keyword, geo_target=f"{city}, {state}", max_questions=max_questions
    )
    faq_list = []

    for q in questions:
        print(f"Generating answer for: {q}")
        answer = generate_answer(q, business_name, city, state)
        faq_list.append((q, answer))

    output_file = os.path.join(output_dir, f"{business_name} - FAQs.html")
    print("Output path:", output_file)

    write_html_accordion(faq_list, business_name, output_file)
    print(f"✅ Saved FAQ HTML to: {output_file}")
