import configparser
from datetime import datetime
from time import sleep
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
                        print(event["org"]["login"], event["type"])
                        if event["org"]["login"] in orgs:
                            events.append(event)

            page += 1

    return events

def getRepoEvents(org: string, startTime: datetime, endTime: datetime, member_contributions: dict):
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
            # check if actor is in member_contributions
                if event['actor']['login'] not in member_contributions:
                    continue
                elif event['type'] == 'IssueCommentEvent': 
                    member_contributions = handle_issue_comment_event(event, member_contributions)
                elif event['type'] == 'IssuesEvent': 
                    member_contributions = handle_issue_event(event, member_contributions)
                elif event['type'] == 'PullRequestEvent': 
                    member_contributions = handle_pull_request_event(event, member_contributions)
        
        page += 1
    
    return member_contributions

def handle_issue_comment_event(event, member_contributions: dict):
    # get link of issue
    link = event['payload']['issue']['html_url']

    if 'pull_request' in event['payload']['issue']:
        member_contributions[event['actor']['login']]['prs'].add(link)
    else:
        member_contributions[event['actor']['login']]['issues'].add(link)

    return member_contributions

def handle_issue_event(event, member_contributions: dict):
    # get link of issue
    link = event['payload']['issue']['html_url']

    member_contributions[event['actor']['login']]['issues'].add(link)

    return member_contributions

def handle_pull_request_event(event, member_contributions: dict):
    # get link of issue
    link = event['payload']['pull_request']['html_url']

    member_contributions[event['actor']['login']]['prs'].add(link)

    return member_contributions

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
