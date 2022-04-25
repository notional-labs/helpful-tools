import configparser
import requests
import commits
from datetime import datetime, date, time 

c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')

GITHUB_TOKEN = str(c["GITHUB"]["github_token"])

headers = {'Authorization': 'token {}'.format(GITHUB_TOKEN), 'Accept': 'application/vnd.github.v3+json'}
org = "notional-labs"

def new_member_contribution_struct():
    return {
        'commits' : 0,
        'issues' : 0,
        'pr' : 0,
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

repos_list = get_all_repos_name(org)
member_contributions = get_all_members(org)

today_beginning = datetime.combine(date.today(), time()).isoformat()
member_contributions = commits.retrieve_commits_all(org, today_beginning, repos_list, member_contributions)

print(member_contributions)