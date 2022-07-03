import datetime
from copy import deepcopy

def compareView(members):
    header = "╔══════════════════════╦═════════════╦════════════╦═════════════════╦════════════════╗\n║        Member        ║   Commits   ║   Issues   ║  Pull Requests  ║  Active Repos  ║\n╠══════════════════════╬═════════════╬════════════╬═════════════════╬════════════════╣\n"
    row1 = ""
    row2 = ""
    for member in members:
        if len(row1) + len(header) <= 1900:
            row1 = row1 + "║ {0:<20} ║     {1:>3}     ║     {2:>3}    ║       {3:>3}       ║       {4:>3}      ║\n".format(member, members[member]["commits"]["count"], len(members[member]["issues"]), len(members[member]["prs"]), len(members[member]["activeRepos"]))
        else:
            row2 = row2 + "║ {0:<20} ║     {1:>3}     ║     {2:>3}    ║       {3:>3}       ║       {4:>3}      ║\n".format(member, members[member]["commits"]["count"], len(members[member]["issues"]), len(members[member]["prs"]), len(members[member]["activeRepos"]))
    footer = "╚══════════════════════╩═════════════╩════════════╩═════════════════╩════════════════╝\n"
    if (row2 == ""):
        print("{}{}{}".format(header, row1, footer))
        return "```{}{}{}```".format(header, row1, footer)
    else:
        return "```{}{}{}```\n\n```{}{}{}```".format(header, row1, footer, header, row2, footer)

def detailView(members):
    personal_view = "     ====== PERSONAL VIEW ======\n"
    data = ""

    for member in members:
        data = data + " - {}: \n      * Commits: {}\n      * Issues:\n".format(member, members[member]["commits"]["count"])
        issue = pr = repo = ""
        for i in members[member]["issues"]:
            issue = issue + "            + {}\n".format(i)
        data = data + issue + "      * Pull Requests:\n"
        for i in members[member]["prs"]:
            pr = pr + "            + {}\n".format(i)
        data = data + pr + "      * Active Repos:\n"
        for i in members[member]["activeRepos"]:
            repo = repo + "            + {}\n".format(i)
        data = data + repo + "\n"
    print("{}{}".format(personal_view, data))
    return "{}{}".format(personal_view, data)

def time_print():
    LOCAL_TIMEZONE = datetime.datetime.now(datetime.timezone.utc).astimezone().tzinfo
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return "Current time: {},  {} Time".format(current_time, LOCAL_TIMEZONE)
