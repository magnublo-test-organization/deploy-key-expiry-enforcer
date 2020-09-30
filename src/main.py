#!/usr/bin/python3

import sys
import requests

GITHUB_API_BASE_URL = "https://api.github.com"

if __name__ == "main":

    web_session = requests.session()
    access_token = sys.argv[1]
    web_session.headers["Authorization"] = f"Bearer {access_token}"

    #GET /orgs/:org/repos
    res = requests.get(f"{GITHUB_API_BASE_URL}/orgs/magnublo-test-organization/repos")
    print(res)
