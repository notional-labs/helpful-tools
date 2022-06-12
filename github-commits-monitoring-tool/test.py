
import requests
import github_monitor.github_monitor as github_monitor
GITHUB_TOKEN = "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"
headers = {
    'Authorization': 'token {}'.format(GITHUB_TOKEN), 
    'Accept': 'application/vnd.github.v3+json'
}
'''
def getUserEvent():
    members = github_monitor.fetchMembers("notional-labs")
    memberEvents = {}
    for member in members:
        events = {
            "issueCommentEvent": [],
            "issuesEvent": [],
            "pullRequestEvent": [],
            "PullRequestReviewEvent": [],
            "PullRequestReviewCommentEvent": [],
            "PullRequestReviewThreadEvent": [],
            "PushEvent": []
        }
        page_index = 1
        query = {'page':page_index}
        response = requests.get("https://api.github.com/users/{}/events".format(member), params=query, headers=headers).json()
        for event in response:
            if (event["org"]["login"] == "notional-labs" or event["org"]["login"] == "cosmos" or event["org"]["login"] == "scrtlabs" or event["org"]["login"] == "osmosis-labs"):
                if event["type"] == "PushEvent":
                    events["PushEvent"].append
                print()
            
getUserEvent()
'''
from datetime import datetime, date, time, timedelta
import pytz

startTime = datetime.combine(date.today() - timedelta(30), time()).astimezone(pytz.UTC)
endTime = datetime.combine(date.today() + timedelta(1), time()).astimezone(pytz.UTC)

print(startTime, endTime)

startTime = datetime.combine(date.today() - timedelta(1), time()).astimezone(pytz.UTC)
endTime = datetime.combine(date.today(), time()).astimezone(pytz.UTC)
print(startTime, endTime)