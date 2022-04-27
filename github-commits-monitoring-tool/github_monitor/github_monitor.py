import configparser
import requests
import github_monitor.commits as commits
import github_monitor.github_events as github_events
from datetime import datetime, date, time, timedelta
import pytz

c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')

GITHUB_TOKEN = str(c["GITHUB"]["github_token"])
EVENT_ORGS = list(c["GITHUB"]["github_event_orgs"].split(','))

headers = {'Authorization': 'token {}'.format(GITHUB_TOKEN), 'Accept': 'application/vnd.github.v3+json'}
org = "notional-labs"

def new_member_contribution_struct():
    return {
        'commits' : set(),
        'issues' : 0,
        'prs' : 0,
    }

def get_all_members(org):

    members_list = dict()
    page_index = 1

    while True:
        query = {'per_page':100, 'page':page_index}
        response = requests.get("https://api.github.com/orgs/{}/members".format(org), params=query, headers=headers)

        all_members = response.json()

        if len(all_members) == 0:
            break

        for member in all_members:
            members_list[member["login"]] = new_member_contribution_struct()
        
        page_index += 1
    
    print("get_all_members done")
    
    return members_list

def query_member_contributions():
    member_contributions = get_all_members(org)

    start_utc = datetime.combine(date.today() - timedelta(30), time()).astimezone(pytz.UTC)
    end_utc = datetime.combine(date.today() + timedelta(1), time()).astimezone(pytz.UTC)

    active_repos = github_events.get_active_repos(org, start_utc, end_utc)

    start_utc = datetime.combine(date.today() - timedelta(1), time()).astimezone(pytz.UTC)
    end_utc = datetime.combine(date.today(), time()).astimezone(pytz.UTC)

    member_contributions = commits.retrieve_commits_all(org, start_utc, end_utc, active_repos, member_contributions)
    #member_contributions = commits.retrieve_commits_one_repo(org, "ibc-go", start_utc, end_utc, member_contributions)

    for event_org in EVENT_ORGS:
        member_contributions = github_events.get_daily_events(event_org, start_utc, end_utc, member_contributions)
    
    return commits.get_commits_length(member_contributions)