import configparser
from datetime import datetime
from lzma import PRESET_EXTREME
from dateutil import parser
import string
import requests

c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')
GITHUB_TOKEN = str(c["GITHUB"]["github_token"])

headers = {
    'Authorization': 'token {}'.format(GITHUB_TOKEN), 
    'Accept': 'application/vnd.github.v3+json'
}

def getUserEvents(orgs, startTime: datetime, endTime: datetime, member):
    page = 1
    events = []
    print("starting get event of {}".format(member))
    while True:
        query = {
            "per_page": 100,
            "page": page
        }
        data = requests.get("https://api.github.com/users/{}/events".format(member), params = query, headers = headers)
        if data.status_code != 200:      
            break
        else:
            data = data.json()
            for event in data:
                # check time of event
                createdDate = parser.isoparse(event['created_at'])

                if createdDate >= endTime:
                    continue
                elif createdDate < startTime:
                    break
                else:
                    if "org" in event.keys():
                        if event["org"]["login"] in orgs:
                            events.append(event)

            page += 1

    return events

def getActiveRepos(org: string, startTime: datetime, endTime: datetime):
    
    page = 1
    repos = set()

    while True:
        query = {
            'per_page':100,
            'page':page
        }
        res = requests.get("https://api.github.com/orgs/{}/events".format(org), params=query, headers=headers)

        if res.status_code != 200:
            if res.status_code != 422:
                print("Error in getting events. Status code = {}".format(res.status_code))
            break

        events = res.json()

        if len(events) == 0:
            break

        for event in events:
            # check time of event
            createdDate = parser.isoparse(event['created_at'])

            if createdDate >= endTime:
                continue
            elif createdDate < startTime:
                continue
            else:
                repo_name = event['repo']['name']
                repos.add(repo_name)

        page += 1
    
    #f.close()
    print("getActiveRepos done")

    return repos

def getIssuesandPR(orgs, startTime: datetime, endTime: datetime, member):
    issues = []
    prs = []
    activeRepos = set()
    events = getUserEvents(orgs, startTime, endTime, member)
    for event in events:
        if event["type"] == "IssuesEvent" or event["type"] == "IssueCommentEvent":
            issues.append(event["payload"]["issue"]["url"])
            activeRepos.add(event['repo']['name'])
        elif event["type"] == "PullRequestEvent" or event["type"] == "PullRequestReviewEvent" or event["type"] == "PullRequestReviewCommentEvent" or event["type"] == "PullRequestReviewThreadEvent":
            prs.append(event["payload"]["pull_request"]["url"])
            activeRepos.add(event['repo']['name'])

    print("get issues and prs not in Notional for {} done".format(member))
    return issues, prs, activeRepos




























'''
def getRepoEvents(org: string, startTime: datetime, endTime: datetime, memberContributions: dict):
    page = 1
    while True:
        query = {
            'per_page':100, 
            'page':page
        }
        res = requests.get("https://api.github.com/orgs/{}/events".format(org), params=query, headers=headers)

        if res.status_code != 200:
            if res.status_code == 422:
                print("stop at {} with index = {}".format(org, page))
            else: 
                print("Error code: {} with text: {}".format(res.status_code, res.json()))
            break

        events = res.json()
        for event in events:
            # check time of event
            createdDate = parser.isoparse(event['created_at'])
            if createdDate > endTime:
                continue
            elif createdDate < startTime:
                break
            else:
            # check if actor is in memberContributions
                if event['actor']['login'] not in memberContributions:
                    continue
                elif event['type'] == 'IssueCommentEvent': 
                    memberContributions = handle_issue_comment_event(event, memberContributions)
                elif event['type'] == 'IssuesEvent': 
                    memberContributions = handle_issue_event(event, memberContributions)
                elif event['type'] == 'PullRequestEvent': 
                    memberContributions = handle_pull_request_event(event, memberContributions)
        
        page += 1
    
    return memberContributions

def handle_issue_comment_event(event, memberContributions: dict):
    # get link of issue
    link = event['payload']['issue']['html_url']

    if 'pull_request' in event['payload']['issue']:
        memberContributions[event['actor']['login']]['prs'].add(link)
    else:
        memberContributions[event['actor']['login']]['issues'].add(link)

    return memberContributions

def handle_issue_event(event, memberContributions: dict):
    # get link of issue
    link = event['payload']['issue']['html_url']

    memberContributions[event['actor']['login']]['issues'].add(link)

    return memberContributions

def handle_pull_request_event(event, memberContributions: dict):
    # get link of issue
    link = event['payload']['pull_request']['html_url']

    memberContributions[event['actor']['login']]['prs'].add(link)

    return memberContributions
'''