import datetime
from time import strftime, localtime

def pretty_print_details(member_contributions : dict):
    compare_view = "====== COMPARE VIEW ======\n"
    commits_text = "COMMITs: \n"
    issues_text = "ISSUEs: \n"
    prs_text = "PRs: \n"

    personal_view = "|====== PERSONAL VIEW ======\n"
    personal_commits = ""
    
    for member_name in member_contributions.keys():
        commits_text += "{}: {} \n".format(member_contributions[member_name]['commits'], member_name)
        issues_text += "{}: {} \n".format(member_contributions[member_name]['issues'], member_name)
        prs_text += "{}: {} \n".format(member_contributions[member_name]['prs'], member_name)

        personal_commits += "{}:  \n     COMMITs:{}\n     ISSUEs:{}\n     PRs:{}\n".format(member_name, member_contributions[member_name]['commits'], member_contributions[member_name]['issues'], member_contributions[member_name]['prs'])
    

    return "{}{}\n\n{}\n\n{}\n\n{}{}".format(compare_view, commits_text, issues_text, prs_text, personal_view, personal_commits)

def time_print(str):
    LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "current time = {} in Timezone GMT{}\n\n{}".format(current_time, LOCAL_TIMEZONE, str)