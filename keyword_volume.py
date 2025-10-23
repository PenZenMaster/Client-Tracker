r"""
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
2025-10-23

Version:
v1.06

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.06 - Added type hints and Google-style docstrings
* v1.05 - Added standardized file header, removed emoji from print (Windows compat)
* v1.04 - Fixed proto enum access using .Value("GOOGLE_SEARCH")
* v1.04 - Fully compatible with google-ads v26.0.1
* v1.04 - Fetches live keyword volume for a URL + seed keywords
"""

from typing import List, Tuple, Optional
from google.ads.googleads.client import GoogleAdsClient  # type: ignore[import-untyped]


def fetch_keyword_ideas(
    client: GoogleAdsClient,
    customer_id: str,
    page_url: str,
    seed_keywords: List[str],
    language_code: str = "1000",
    geo_targets: Optional[List[str]] = None,
) -> List[Tuple[str, int]]:
    """Fetch keyword ideas with search volumes from Google Ads API.

    Uses the Keyword Planner API to generate keyword suggestions based on a
    seed URL and keyword list. Returns keywords with average monthly search volumes.

    Args:
        client: Initialized GoogleAdsClient instance with valid credentials.
        customer_id: Google Ads customer ID (10-digit string without hyphens).
        page_url: Target website URL to base keyword research on.
        seed_keywords: List of initial keywords to expand upon.
        language_code: Google Ads language criterion ID. Defaults to "1000" (English).
        geo_targets: List of Google Ads geo target criterion IDs.
            Defaults to ["2840"] (United States).

    Returns:
        List of tuples containing (keyword_text, avg_monthly_searches).
        Example: [("hvac repair", 5400), ("air conditioning", 8100)]

    Example:
        >>> from google.ads.googleads.client import GoogleAdsClient
        >>> client = GoogleAdsClient.load_from_storage("google-ads.yaml")
        >>> results = fetch_keyword_ideas(
        ...     client,
        ...     "1234567890",
        ...     "https://example.com",
        ...     ["hvac repair", "ac service"]
        ... )
        >>> print(results[0])
        ('hvac repair near me', 2400)
    """
    if geo_targets is None:
        geo_targets = ["2840"]
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
