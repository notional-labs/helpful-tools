import configparser
from datetime import datetime
from github_events import getUserEvents
import re
import requests
import json

c = configparser.ConfigParser()
c.read("config.ini", encoding = 'utf-8')

GITHUB_TOKEN = str(c["GITHUB"]["github_token"])
headers = {
    'Authorization': 'token {}'.format(GITHUB_TOKEN), 
    'Accept': 'application/vnd.github.v3+json'
}
    
def getCommits(orgs, startTime: datetime, endTime: datetime, repos, member, commits, activeRepo):
    # inNotional("notional-labs", startTime, endTime, repos, member, activeRepo, value)
    (commits, activeRepo) = notinNotional(orgs, startTime, endTime, member, activeRepo, commits)
    print("get commits history for {} done".format(member))
    return (commits, activeRepo)

def getBranches(org, repo):
    page_index = 1
    branches = list()

    while True:
        query = {'per_page':100, 'page':page_index}
        data = requests.get("https://api.github.com/repos/{}/{}/branches".format(org, repo), params = query, headers = headers).json()

        if len(data) == 0:
            break
        else:
            for branch in data:
                branches.append(branch['name'])
            page_index += 1
    print("Get branches of {} done".format(repo))
    return branches

def inNotional(org, startTime: datetime, endTime: datetime, repos, member, activeRepo, value):
    for repo in repos:
        branches = getBranches(org, repo)

        for branch in branches:
            page_index = 1
            while True:
                query = {
                    'per_page':100,
                    'page':page_index, 
                    'since':startTime.isoformat(), 
                    'until':endTime.isoformat(), 
                    'sha':branch
                }
                res = requests.get("https://api.github.com/repos/{}/{}/commits".format(org, repo), params = query, headers = headers)

                if res.status_code != 200:
                    print("ERROR: fail to fetch repo = {} and branch = {}".format(repo, branch))
                    # log error to bot
                    return value
                else:
                    commits = res.json()
                    if len(commits) == 0:
                        break
                    #filter commit to recognized member of org
                    for commit in commits:
                        author = commit['author']['login']
                        if author != member:
                            continue
                        else:
                            value['count'] = value['count'] + 1
                            value['sha'].append(commit['sha'])
                    
                    page_index += 1

        if (value['count']):
            activeRepo.add(repo)
    print("get commit in Notional for {} done".format(member))

def notinNotional(orgs, startTime: datetime, endTime: datetime, member, activeRepo, value):
    events = getUserEvents(orgs, startTime, endTime, member)
    for event in events:
        if event["type"] == "PushEvent":
            for commit in event["payload"]["commits"]:
                if commit["distinct"] == "true":
                    value['count'] = value['count'] + 1
                    value['sha'].append(commit['sha'])
        
            activeRepo.add(event['repo']['name'].split('/')[1])
    print("get commit not in Notional for {} done".format(member))
    return (value, activeRepo)