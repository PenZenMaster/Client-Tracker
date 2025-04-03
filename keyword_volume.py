# Author: Skippy the Magnificent along with that dumb ape, George Penzenik
# Version: 1.00
# Date Modified: 23:42 04/03/2025
# Comment:
#  - Initial version to connect to Google Ads API and fetch keyword volume for a URL + seed keywords

import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.v15.enums.types.keyword_plan_network import KeywordPlanNetwork
from google.ads.googleads.v15.services.types.keyword_plan_idea_service import GenerateKeywordIdeasRequest, KeywordAndUrlSeed
from google.ads.googleads.v15.services.services.keyword_plan_idea_service import KeywordPlanIdeaServiceClient
from google.ads.googleads.v15.resources.types import KeywordPlanHistoricalMetrics


def fetch_keyword_ideas(client, customer_id, page_url, seed_keywords, language_code="1000", geo_targets=["2840"]):
    """
    Fetch keyword ideas from Google Ads API.
    language_code: default is English (1000)
    geo_targets: default is United States (2840)
    """
    service = client.get_service("KeywordPlanIdeaService")

    request = GenerateKeywordIdeasRequest(
        customer_id=customer_id,
        language=client.get_service("GoogleAdsService").language_constant_path(language_code),
        geo_target_constants=[client.get_service("GoogleAdsService").geo_target_constant_path(gt) for gt in geo_targets],
        keyword_plan_network=KeywordPlanNetwork.GOOGLE_SEARCH,
        keyword_and_url_seed=KeywordAndUrlSeed(
            url=page_url,
            keywords=seed_keywords
        )
    )

    print("\n📊 Keyword Ideas:")
    response = service.generate_keyword_ideas(request=request)

    results = []
    for idea in response:
        keyword_text = idea.text
        metrics = idea.keyword_idea_metrics
        avg_searches = metrics.avg_monthly_searches if metrics else 0
        print(f"- {keyword_text}: {avg_searches} searches/month")
        results.append((keyword_text, avg_searches))

    return results


if __name__ == "__main__":
    google_ads_config_path = "google-ads.yaml"  # Make sure this YAML file is set up properly
    client = GoogleAdsClient.load_from_storage(google_ads_config_path)

    customer_id = "INSERT_YOUR_CUSTOMER_ID"
    seed_keywords = ["HVAC repair", "air conditioning install", "furnace service"]
    page_url = "https://www.tri-stateheating.com/"

    fetch_keyword_ideas(client, customer_id, page_url, seed_keywords)
