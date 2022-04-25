import configparser
import requests

c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')

GITHUB_TOKEN = str(c["GITHUB"]["github_token"])

headers = {'Authorization': 'token {}'.format(GITHUB_TOKEN), 'Accept': 'application/vnd.github.v3+json'}

def retrieve_commits_one_repo(org, repo, since, member_contributions):
    
    page_index = 1

    while True:
        query = {'per_page':100, 'page':page_index, 'since':since}
        res = requests.get("https://api.github.com/repos/{}/{}/commits".format(org, repo), params=query, headers=headers)

        if res.status_code != 200:
            print("ERROR: fail to fetch repo {}".format(repo))
            # log error to bot
            return member_contributions

        all_commits = res.json()

        if len(all_commits) == 0:
            break
        
        #filter commit to recognized member of org
        for commit in all_commits:
            commit_author = commit['author']['login']

            if commit_author not in member_contributions:
                continue

            member_contributions[commit_author]['commits'] += 1
        
        page_index += 1
    
    print("retrieve_commits_one_repo done in repo {}".format(repo))

    return member_contributions

def retrieve_commits_all(org, since, repos_list, member_contributions):
    for repo in repos_list:
        member_contributions = retrieve_commits_one_repo(org, repo, since, member_contributions)
    
    print("retrieve_commits_all done")
    
    return member_contributions