import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)


def fetch_paa_questions(keyword, location="us"):
    print(f"Fetching PAA questions for: {keyword}")
    params = {
        "engine": "google",
        "q": keyword,
        "hl": "en",
        "gl": location,
        "api_key": SERPAPI_KEY,
    }
    res = requests.get("https://serpapi.com/search", params=params)
    print("SerpAPI status code:", res.status_code)

    try:
        data = res.json()
    except Exception as e:
        print("Error decoding SerpAPI response:", e)
        return []

    if "error" in data:
        print("SerpAPI error:", data["error"])
        return []

    questions = []

    if "related_questions" in data:
        for q in data["related_questions"]:
            question = q.get("question")
            if question and question not in questions:
                questions.append(question)
            if len(questions) >= 20:
                break

    return questions[:20]


def generate_answer(question, business_name, city, state):
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
    return response.choices[0].message.content.strip()


def write_html_accordion(faq_list, business_name, output_path):
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{business_name} - FAQs</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: #f9f9f9;
            padding: 20px;
        }}
        .accordion {{
            background-color: #fff;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
        .accordion-item {{
            margin-bottom: 10px;
        }}
        .accordion-header {{
            background-color: #eee;
            cursor: pointer;
            padding: 10px;
            border-radius: 6px;
            transition: 0.3s;
        }}
        .accordion-header:hover {{
            background-color: #ddd;
        }}
        .accordion-content {{
            display: none;
            padding: 10px;
            margin-top: 5px;
        }}
    </style>
</head>
<body>
    <h1>{business_name} - People Also Ask</h1>
    <div class="accordion">
"""
    for i, (q, a) in enumerate(faq_list):
        html += f"""
        <div class="accordion-item">
            <div class="accordion-header" onclick="toggleContent('content{i}')">{q}</div>
            <div class="accordion-content" id="content{i}">{a}</div>
        </div>
"""
    html += """
    </div>
    <script>
        function toggleContent(id) {
            var x = document.getElementById(id);
            if (x.style.display === "block") {
                x.style.display = "none";
            } else {
                x.style.display = "block";
            }
        }
    </script>
</body>
</html>"""

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def run_faq_generator(client_config):
    business_name = client_config["name"]
    city = client_config["city"]
    state = client_config["state"]
    keyword = client_config["seed_keyword"]
    output_root = client_config["output_root"]

    output_dir = os.path.join(output_root, business_name, "G Site")
    os.makedirs(output_dir, exist_ok=True)

    questions = fetch_paa_questions(keyword)
    faq_list = []

    for q in questions:
        answer = generate_answer(q, business_name, city, state)
        faq_list.append((q, answer))

    output_file = os.path.join(output_dir, f"{business_name} - FAQs.html")
    print("Output path:", output_file)

    write_html_accordion(faq_list, business_name, output_file)
    print(f"Saved FAQ HTML to: {output_file}")
