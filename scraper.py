r"""
Module/Script Name: scraper.py
Path: E:\projects\Project Tracking\scraper.py

Description:
Website content scraper using BeautifulSoup. Extracts text from web pages
for SEO analysis and content generation, removing scripts, styles, and navigation.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2024-01-15

Last Modified Date:
2025-10-23

Version:
v1.01

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.01 - Added standardized file header
* v1.00 - Initial release with BeautifulSoup scraping
"""

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
