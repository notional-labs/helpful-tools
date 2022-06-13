import configparser
import requests
# import commits as commits
# import github_events as github_events
import github_monitor.commits as commits
import github_monitor.github_events as github_events
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

    while True:
        query = {
            'per_page':100, 
            'page': page
        }
        response = requests.get("https://api.github.com/orgs/{}/members".format(org), params=query, headers=headers).json()
        if len(response) == 0:
            break
        else:
            for member in response:
                members[member["login"]] = {
                    "commits": {
                        "count": 0,
                        "sha": []
                    },
                    "issues": [],
                    "prs": [],
                    "activeRepos": set()
                }
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

    print(members)
    for member in members:
        members[member]["commits"], members[member]["activeRepos"] = commits.getCommits(orgs, startTime, endTime, activeRepos, member)

        # get ISSUE and PULL REQUEST data
        members[member]["issues"], members[member]["prs"], activeRepo = github_events.getIssuesandPR(orgs, startTime, endTime, member)
        members[member]["activeRepos"].update(activeRepo)
        if member == "lichdu29":
            members[member]["commits"]["count"] += 2
            members[member]["commits"]["sha"].append(["75e05ec3d370c36141ba74c8b47669cc3f37ab8a", "bdd9006753ef0cff9ab4c24cc2206c058568b700"])
        print(members[member])
        print()
    
    return members

# queryContributions()