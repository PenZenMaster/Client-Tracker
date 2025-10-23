"""
Module/Script Name: keyword_volume.py
Path: E:\projects\Project Tracking\keyword_volume.py

Description:
Google Ads API integration for keyword research. Fetches keyword ideas with
search volumes using Keyword Planner API for given URL and seed keywords.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved

Created Date:
2025-04-03

Last Modified Date:
2025-10-22

Version:
v1.05

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.05 - Added standardized file header, removed emoji from print (Windows compat)
* v1.04 - Fixed proto enum access using .Value("GOOGLE_SEARCH")
* v1.04 - Fully compatible with google-ads v26.0.1
* v1.04 - Fetches live keyword volume for a URL + seed keywords
"""

from google.ads.googleads.client import GoogleAdsClient


def fetch_keyword_ideas(
    client,
    customer_id,
    page_url,
    seed_keywords,
    language_code="1000",
    geo_targets=["2840"],
):
    """
    Fetch keyword ideas from Google Ads API.
    language_code: default is English (1000)
    geo_targets: default is United States (2840)
    """
    keyword_plan_service = client.get_service("KeywordPlanIdeaService")
    google_ads_service = client.get_service("GoogleAdsService")

    # Dynamically load message and enum types
    GenerateKeywordIdeasRequest = client.get_type("GenerateKeywordIdeasRequest")
    KeywordAndUrlSeed = client.get_type("KeywordAndUrlSeed")
    KeywordPlanNetworkEnum = client.get_type("KeywordPlanNetworkEnum")

    request = GenerateKeywordIdeasRequest(
        customer_id=customer_id,
        language=google_ads_service.language_constant_path(language_code),
        geo_target_constants=[
            google_ads_service.geo_target_constant_path(gt) for gt in geo_targets
        ],
        keyword_plan_network=KeywordPlanNetworkEnum.Value("GOOGLE_SEARCH"),
        keyword_and_url_seed=KeywordAndUrlSeed(
            url=page_url,
            keywords=seed_keywords,
        ),
    )

    print("\n[INFO] Keyword Ideas:")
    response = keyword_plan_service.generate_keyword_ideas(request=request)

    results = []
    for idea in response:
        keyword_text = idea.text
        metrics = idea.keyword_idea_metrics
        avg_searches = metrics.avg_monthly_searches if metrics else 0
        print(f"- {keyword_text}: {avg_searches} searches/month")
        results.append((keyword_text, avg_searches))

    return results


if __name__ == "__main__":
    google_ads_config_path = "google-ads.yaml"
    client = GoogleAdsClient.load_from_storage(google_ads_config_path)

    customer_id = (
        "INSERT_YOUR_CUSTOMER_ID"  # ← Replace with your real ID like "1234567890"
    )
    seed_keywords = ["HVAC repair", "air conditioning install", "furnace service"]
    page_url = "https://www.tri-stateheating.com/"

    fetch_keyword_ideas(client, customer_id, page_url, seed_keywords)
