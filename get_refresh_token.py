# Author: Skippy the Magnificent (and that ape George)
# Version: 1.00
# Date Modified: 04/03/2025
# Comment: Launches OAuth flow and generates refresh token for Google Ads API

from google_auth_oauthlib.flow import InstalledAppFlow


def generate_refresh_token():
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": "37156535763-79hajfra02dtocpef812lhg3fgakgfqi.apps.googleusercontent.com",
                "client_secret": "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",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }
        },
        scopes=["https://www.googleapis.com/auth/adwords"],
    )

    creds = flow.run_local_server(
        port=8080, prompt="consent", authorization_prompt_message=""
    )
    print("\n🎉 SUCCESS! Paste the following into your google-ads.yaml:\n")
    print(f"refresh_token: {creds.refresh_token}")


if __name__ == "__main__":
    generate_refresh_token()
