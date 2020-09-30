#!/usr/bin/python3
import json
import sys
import requests

GITHUB_API_BASE_URL = "https://api.github.com"

if __name__ == "__main__":

    web_session = requests.session()
    access_token = sys.argv[1]
    #web_session.headers["Authorization"] = f"Bearer {access_token}"

    #GET /orgs/:org/repos
    res = web_session.get(f"{GITHUB_API_BASE_URL}/orgs/magnublo-test-organization/repos")

    repositories = json.loads(res.text)
    deploy_key_api_urls = [r["keys_url"] for r in repositories]
    print(res.text)
