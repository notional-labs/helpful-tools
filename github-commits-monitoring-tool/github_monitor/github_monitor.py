import configparser
import requests
# import github_monitor.commits as commits
import commits 
import github_events
# import github_monitor.github_events as github_events
from datetime import datetime, date, time, timedelta
import pytz

c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')

GITHUB_TOKEN = str(c["GITHUB"]["github_token"])
orgs = list(c["GITHUB"]["github_event_orgs"].split(','))
headers = {
    'Authorization': 'token {}'.format(GITHUB_TOKEN), 
    'Accept': 'application/vnd.github.v3+json'
}

org = "notional-labs"

def fetchMembers(org):
    members = dict()
    page = 1
    contribution = {
        "commits": {
            "count": 0,
            "sha": []
        },
        "issues": [],
        "prs": [],
        "activeRepos": set()
    }

    while True:
        query = {
            'per_page':100, 
            'page':page
        }
        response = requests.get("https://api.github.com/orgs/{}/members".format(org), params=query, headers=headers).json()
        print(response)
        print(headers)
        if len(response) == 0:
            break
        else:
            for member in response:
                print(member)
                members[member["login"]] = contribution
            page += 1
    
    print("Fetched {} members".format(len(members)))
    return members

def queryContributions():
    members = fetchMembers(org)

    # get all Notional active repos within 1 month
    startTime = datetime.combine(date.today() - timedelta(30), time()).astimezone(pytz.UTC)
    endTime = datetime.combine(date.today() + timedelta(1), time()).astimezone(pytz.UTC)
    activeRepos = github_events.getActiveRepos(org, startTime, endTime)
    print("Fetched {} repos".format(len(activeRepos)))
    # get all commits in 1 day
    startTime = datetime.combine(date.today() - timedelta(1), time()).astimezone(pytz.UTC)
    endTime = datetime.combine(date.today(), time()).astimezone(pytz.UTC)
    for member in members:
        (members[member]["commits"], members[member]["activeRepos"]) = commits.getCommits(orgs, startTime, endTime, activeRepos, member, members[member]["commits"], members[member]["activeRepos"])
        print(members[member])
        print()

    # get ISSUE and PULL REQUEST data
    # for org in orgs:
    #    members = github_events.getRepoEvents(org, startTime, endTime, members)
    
    return members

queryContributions()