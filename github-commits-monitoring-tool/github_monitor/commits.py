import configparser
from datetime import datetime
import requests
from copy import deepcopy
import json

c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')

GITHUB_TOKEN = str(c["GITHUB"]["github_token"])

headers = {'Authorization': 'token {}'.format(GITHUB_TOKEN), 'Accept': 'application/vnd.github.v3+json'}

def retrieve_commits_one_repo(org, repo, start_utc: datetime, end_utc: datetime, member_contributions):
    
    # f = open("temp.txt", "a")

    # get all branches of a repo
    branches = retrieve_branches_all(org, repo)

    for branch in branches:
        page_index = 1
        
        while True:
            query = {'per_page':100, 'page':page_index, 'since':start_utc.isoformat(), 'until':end_utc.isoformat(), 'sha':branch}
            res = requests.get("https://api.github.com/repos/{}/{}/commits".format(org, repo), params=query, headers=headers)

            if res.status_code != 200:
                print("ERROR: fail to fetch repo={} and branch={}".format(repo, branch))
                # log error to bot
                return member_contributions

            all_commits = res.json()

            if len(all_commits) == 0:
                break
            
            #filter commit to recognized member of org
            for commit in all_commits:
                # f.write(json.dumps(commit) + '\n')
                commit_author = commit['author']['login']

                if commit_author not in member_contributions:
                    continue

                commit_sha = '{}/{}'.format(repo, commit['sha'])
                member_contributions[commit_author]['commits'].add(commit_sha)
            
            page_index += 1
    
    # f.close()
    print("retrieve_commits_one_repo done in repo {}".format(repo))

    return member_contributions

def retrieve_branches_all(org, repo):

    page_index = 1
    branches_list = list()

    while True:
        query = {'per_page':100, 'page':page_index}
        res = requests.get("https://api.github.com/repos/{}/{}/branches".format(org, repo), params=query, headers=headers)

        branches = res.json()

        if len(branches) == 0:
            break
        
        for branch in branches:
            branches_list.append(branch['name'])
        
        page_index += 1
    
    print("retrieve_branches_all done")

    return branches_list

def retrieve_commits_all(org, start_utc: datetime, end_utc: datetime, repos_list, member_contributions):
    for repo in repos_list:
        member_contributions = retrieve_commits_one_repo(org, repo, start_utc, end_utc, member_contributions)
    
    print("retrieve_commits_all done")
    
    return member_contributions

# HELPER FUNCTIONS FOR EASIER PRINT
def get_commits_length(member_contributions: dict):
    member_contributions_with_commits_as_int = deepcopy(member_contributions)

    for member_key in member_contributions.keys():
        member_contributions_with_commits_as_int[member_key]['commits'] = len(member_contributions[member_key]['commits'])
    
    return member_contributions_with_commits_as_int