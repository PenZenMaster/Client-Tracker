import requests
from bs4 import BeautifulSoup

def scrape_website_text(url, max_paragraphs=20):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[ERROR] Failed to retrieve content from {url}: {e}")
        return ""

    soup = BeautifulSoup(response.text, "lxml")

    for element in soup(["script", "style", "header", "footer", "nav", "form"]):
        element.decompose()

    text_blocks = []
    for tag in soup.find_all(["h1", "h2", "p"]):
        text = tag.get_text(strip=True)
        if text:
            text_blocks.append(text)

    return "\n".join(text_blocks[:max_paragraphs])