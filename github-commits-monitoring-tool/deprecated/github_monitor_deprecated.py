import configparser
import requests

c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')

GITHUB_TOKEN = str(c["GITHUB"]["github_token"])

headers = {'Authorization': 'token {}'.format(GITHUB_TOKEN), 'Accept': 'application/vnd.github.v3+json'}
org = "notional-labs"

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