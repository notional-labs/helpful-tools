import configparser
from datetime import datetime
from dateutil import parser
import string
import requests
import json

c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')

GITHUB_TOKEN = str(c["GITHUB"]["github_token"])

headers = {
    'Authorization': 'token {}'.format(GITHUB_TOKEN), 
    'Accept': 'application/vnd.github.v3+json'
}

def getRepoEvents(org: string, startTime: datetime, endTime: datetime, member_contributions: dict):
    
    page_index = 1
    f = open("temp.txt", "a")

    while True:
        query = {'per_page':100, 'page':page_index}
        path = "https://api.github.com/orgs/{}/events".format(org)
        res = requests.get(path, params=query, headers=headers)

        events = res.json()

        for event in events:

            # check time of event
            event_create_date = parser.isoparse(event['created_at'])

            if event_create_date >= endTime:
                continue

            if event_create_date < startTime:
                f.close()
                return member_contributions

            f.write(json.dumps(event) + '\n')
                
            # check if actor is in member_contributions
            if event['actor']['login'] not in member_contributions:
                continue

            if event['type'] == 'PushEvent': member_contributions = handle_push_event(event, member_contributions)
            if event['type'] == 'IssueCommentEvent': member_contributions = handle_issue_comment_event(event, member_contributions)
            if event['type'] == 'IssuesEvent': member_contributions = handle_issue_event(event, member_contributions)
            if event['type'] == 'PullRequestEvent': member_contributions = handle_pull_request_event(event, member_contributions)
        
        page_index += 1

def handle_push_event(event, member_contributions: dict):
    commits = event['payload']['commits']

    for commit in commits:
        # filter commits
        if commit['author']['email'].find(event['actor']['login']) == -1:
            continue

        # add commits
        commit_sha = '{}/{}'.format(event['repo']['name'], commit['sha'])
        member_contributions[event['actor']['login']]['commits'].add(commit_sha)

    return member_contributions

def handle_issue_comment_event(event, member_contributions: dict):
    member_contributions[event['actor']['login']]['issues'] += 1

    return member_contributions

def handle_issue_event(event, member_contributions: dict):
    member_contributions[event['actor']['login']]['issues'] += 1

    return member_contributions

def handle_pull_request_event(event, member_contributions: dict):
    member_contributions[event['actor']['login']]['prs'] += 1

    return member_contributions