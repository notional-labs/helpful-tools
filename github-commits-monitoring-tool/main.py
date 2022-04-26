import configparser
import requests
import commits
import github_events
from datetime import datetime, date, time, timedelta
import pytz
from typing import Callable

c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')

GITHUB_TOKEN = str(c["GITHUB"]["github_token"])

headers = {'Authorization': 'token {}'.format(GITHUB_TOKEN), 'Accept': 'application/vnd.github.v3+json'}
org = "notional-labs"

def new_member_contribution_struct():
    return {
        'commits' : set(),
        'issues' : 0,
        'prs' : 0,
    }

def get_all_repos_name(org):
    
    repos_list = list()
    page_index = 1

    while True:
        query = {'per_page':100, 'page':page_index}
        response = requests.get("https://api.github.com/orgs/{}/repos".format(org), params=query, headers=headers)

        all_repos = response.json()

        if len(all_repos) == 0:
            break
        
        for repo in all_repos:
            repos_list.append(repo["name"])
        
        page_index += 1
    
    print("get_all_repos_name done")
    
    return repos_list

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
    member_contributions = github_events.get_daily_events(org, start_utc, end_utc, member_contributions)
    
    print(commits.get_commits_length(member_contributions))

def benchmark(func: Callable):
    start_time = datetime.now().timestamp()
    func()
    total_execution_time = datetime.now().timestamp() - start_time

    print("Total execution time in milliseconds = {}".format(total_execution_time * 1000))

benchmark(query_member_contributions)