#!/usr/bin/python3
import datetime
import json
import sys
import time
from math import floor
from time import strptime
from typing import Dict, Set

import requests

GITHUB_API_BASE_URL = "https://api.github.com"
ORG_NAME = "magnublo-test-organization"
DEPLOY_MAX_AGE_DAYS = 365


def get_repository_collaborators(web_session: requests.Session, repository: Dict) -> Dict:
    repo_name = repository["name"]
    collaborators_url = f"{GITHUB_API_BASE_URL}/repos/{ORG_NAME}/{repo_name}/collaborators"
    res = web_session.get(collaborators_url)
    collaborators = json.loads(res.text)
    return collaborators


def get_repository_deploy_keys(web_session: requests.Session, repository: Dict) -> Dict:
    repo_name = repository["name"]
    deploy_key_api_url = f"{GITHUB_API_BASE_URL}/repos/{ORG_NAME}/{repo_name}/keys"
    res = web_session.get(deploy_key_api_url)
    deploy_keys = json.loads(res.text)
    return deploy_keys


def get_collaborator_emails(web_session: requests.Session, collaborators: Dict) -> Set[str]:
    emails = []

    for collaborator in collaborators:
        collaborator_username = collaborator["login"]
        res = web_session.get(f"{GITHUB_API_BASE_URL}/users/{collaborator_username}")
        collaborator_info = json.loads(res.text)
        email = collaborator_info["email"]
        emails.append(email)

    return set(emails)


def notify_collaborators(collaborator_emails: Set[str], days_until_expiry: int):
    raise NotImplementedError()


def notify_expiry(deploy_key: Dict, collaborator_emails: Set[str]):
    key_creation_date_struct = strptime(deploy_key["created_at"], "%Y-%m-%dT%H:%M:%SZ")
    key_creation_date = datetime.datetime.fromtimestamp(time.mktime(key_creation_date_struct))
    seconds_since_creation = (datetime.datetime.now() - key_creation_date).seconds  # I know I mess up time zone differences here
    days_since_creation = floor(seconds_since_creation / (3600*24))

    days_until_expiry = 365 - days_since_creation

    if days_until_expiry < 10:  # If less than 10 days to expiry, notify all collaborators every day
        notify_collaborators(collaborator_emails, days_until_expiry)
    elif days_until_expiry < 30 and days_until_expiry % 7 == 0:  # If less than 30 days to expiry, notify all collabors weekly
        notify_collaborators(collaborator_emails, days_until_expiry)


if __name__ == "__main__":

    web_session = requests.session()
    access_token = sys.argv[1]
    web_session.headers["Authorization"] = f"token {access_token}"

    res = web_session.get(f"{GITHUB_API_BASE_URL}/orgs/magnublo-test-organization/repos")

    repositories = json.loads(res.text)

    for repository in repositories:
        collaborators = get_repository_collaborators(web_session, repository)
        deploy_keys = get_repository_deploy_keys(web_session, repository)
        collaborator_emails = get_collaborator_emails(web_session, collaborators)
        for deploy_key in deploy_keys:
            notify_expiry(deploy_key, collaborator_emails)
