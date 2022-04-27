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

headers = {'Authorization': 'token {}'.format(GITHUB_TOKEN), 'Accept': 'application/vnd.github.v3+json'}

def get_daily_events(org: string, start_utc: datetime, end_utc: datetime, member_contributions: dict):
    
    page_index = 1
    #f = open("temp.txt", "a")

    while True:
        query = {'per_page':100, 'page':page_index}
        path = "https://api.github.com/orgs/{}/events".format(org)
        res = requests.get(path, params=query, headers=headers)

        if res.status_code != 200:
            if res.status_code == 422:
                print("stop at {} with index = {}".format(org, page_index))
            else: print("Error code: {} with text: {}".format(res.status_code, res.json()))
            
            break

        events = res.json()

        for event in events:

            # check time of event
            event_create_date = parser.isoparse(event['created_at'])

            if event_create_date >= end_utc:
                continue

            if event_create_date < start_utc:
                #f.close()
                return member_contributions

            #f.write(json.dumps(event) + '\n')
                
            # check if actor is in member_contributions
            if event['actor']['login'] not in member_contributions:
                continue

            if event['type'] == 'IssueCommentEvent': member_contributions = handle_issue_comment_event(event, member_contributions)
            if event['type'] == 'IssuesEvent': member_contributions = handle_issue_event(event, member_contributions)
            if event['type'] == 'PullRequestEvent': member_contributions = handle_pull_request_event(event, member_contributions)
        
        page_index += 1
    
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

def get_active_repos(org: string, start_utc: datetime, end_utc: datetime):
    
    page_index = 1
    repos = set()
    #f = open("temp.txt", "a")

    while True:
        query = {'per_page':100, 'page':page_index}
        path = "https://api.github.com/orgs/{}/events".format(org)
        res = requests.get(path, params=query, headers=headers)

        if res.status_code != 200:
            if res.status_code != 422:
                print("Error in getting events. Status code = {}".format(res.status_code))

            break

        events = res.json()

        if len(events) == 0:
            break

        for event in events:
            #f.write(json.dumps(event) + '\n')
            # check time of event
            event_create_date = parser.isoparse(event['created_at'])

            if event_create_date >= end_utc:
                continue

            if event_create_date < start_utc:
                continue

            repo_name = event['repo']['name'].split('/')[1]
            repos.add(repo_name)

        page_index += 1
    
    #f.close()
    print("get_active_repos done")

    return repos