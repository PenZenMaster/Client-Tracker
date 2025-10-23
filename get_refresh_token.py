r"""
Module/Script Name: get_refresh_token.py
Path: E:\projects\Project Tracking\get_refresh_token.py

Description:
OAuth 2.0 flow launcher for Google Ads API. Generates refresh token for API
authentication using InstalledAppFlow with local server callback.

Author(s):
Rank Rocket Co (C) Copyright 2025 - All Rights Reserved
Original Authors: Skippy the Magnificent, George Penzenik

Created Date:
2025-04-03

Last Modified Date:
2025-10-23

Version:
v1.01

License:
CC BY-SA 4.0 - https://creativecommons.org/licenses/by-sa/4.0/

Comments:
* v1.01 - Added standardized file header
* v1.00 - Initial release with OAuth flow for Google Ads
"""

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
