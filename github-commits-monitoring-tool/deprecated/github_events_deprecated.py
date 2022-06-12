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

def getRepoEvents(org: string, startTime: datetime, endTime: datetime, memberContributions: dict):
    
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
                return memberContributions

            f.write(json.dumps(event) + '\n')
                
            # check if actor is in memberContributions
            if event['actor']['login'] not in memberContributions:
                continue

            if event['type'] == 'PushEvent': memberContributions = handle_push_event(event, memberContributions)
            if event['type'] == 'IssueCommentEvent': memberContributions = handle_issue_comment_event(event, memberContributions)
            if event['type'] == 'IssuesEvent': memberContributions = handle_issue_event(event, memberContributions)
            if event['type'] == 'PullRequestEvent': memberContributions = handle_pull_request_event(event, memberContributions)
        
        page_index += 1

def handle_push_event(event, memberContributions: dict):
    commits = event['payload']['commits']

    for commit in commits:
        # filter commits
        if commit['author']['email'].find(event['actor']['login']) == -1:
            continue

        # add commits
        commit_sha = '{}/{}'.format(event['repo']['name'], commit['sha'])
        memberContributions[event['actor']['login']]['commits'].add(commit_sha)

    return memberContributions

def handle_issue_comment_event(event, memberContributions: dict):
    memberContributions[event['actor']['login']]['issues'] += 1

    return memberContributions

def handle_issue_event(event, memberContributions: dict):
    memberContributions[event['actor']['login']]['issues'] += 1

    return memberContributions

def handle_pull_request_event(event, memberContributions: dict):
    memberContributions[event['actor']['login']]['prs'] += 1

    return memberContributions