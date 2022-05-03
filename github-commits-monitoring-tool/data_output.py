import datetime
from copy import deepcopy

def pretty_print_compare_view(member_contributions : dict):

    prepared_member_contributions = get_commits_length(member_contributions)
    prepared_member_contributions = get_issues_and_prs_length(prepared_member_contributions)

    compare_view = "====== COMPARE VIEW ======\n"
    commits_text = "COMMITs: \n"
    issues_text = "ISSUEs: \n"
    prs_text = "PRs: \n"
    
    for member_name in prepared_member_contributions.keys():
        commits_text += "{}: {} \n".format(prepared_member_contributions[member_name]['commits'], member_name)
        issues_text += "{}: {} \n".format(prepared_member_contributions[member_name]['issues'], member_name)
        prs_text += "{}: {} \n".format(prepared_member_contributions[member_name]['prs'], member_name)
    

    return "{}{}\n\n{}\n\n{}".format(compare_view, commits_text, issues_text, prs_text)

def pretty_print_personal_view(member_contributions : dict):

    prepared_member_contributions = get_commits_length(member_contributions)

    personal_view = "|====== PERSONAL VIEW ======\n"
    personal = ""

    for member_name in prepared_member_contributions.keys():
        personal_issues_print = "\n"
        personal_prs_print = "\n"

        personal_issues = prepared_member_contributions[member_name]['issues']
        personal_prs = prepared_member_contributions[member_name]['prs']

        for issue in personal_issues:
            personal_issues_print += "        * {}\n".format(issue)
        
        for pr in personal_prs:
            personal_prs_print += "        * {}\n".format(pr)

        personal += "{}:  \n     COMMITs:{}\n     ISSUEs:{}\n     PRs:{}\n".format(member_name, prepared_member_contributions[member_name]['commits'], personal_issues_print, personal_prs_print)
    
    return "{}{}".format(personal_view, personal)

def time_print():
    LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "current time = {} in Timezone {}".format(current_time, LOCAL_TIMEZONE)

# HELPER FUNCTIONS FOR EASIER PRINT
def get_commits_length(member_contributions: dict):
    member_contributions_with_commits_as_int = deepcopy(member_contributions)

    for member_key in member_contributions.keys():
        member_contributions_with_commits_as_int[member_key]['commits'] = len(member_contributions[member_key]['commits'])
    
    return member_contributions_with_commits_as_int

def get_issues_and_prs_length(member_contributions: dict):
    member_contributions_with_issues_and_prs_as_int = deepcopy(member_contributions)

    for member_key in member_contributions.keys():
        member_contributions_with_issues_and_prs_as_int[member_key]['issues'] = len(member_contributions[member_key]['issues'])
        member_contributions_with_issues_and_prs_as_int[member_key]['prs'] = len(member_contributions[member_key]['prs'])
    
    return member_contributions_with_issues_and_prs_as_int