# chain-helpful-tools
This is a collection of helpful tools

# github-commits-monitoring-tool
Discord monitor bot

<details>
  <summary>List of available commands:</summary>

1. no commands

</details>  

## How it works?
1. At exactly 1 am everyday, the code will be invoked and start gather member activities on github
2. It will first query all members belong to notional-labs

### A. Commits query
1. It will query events (in close past) happened in notional-labs to determine active repositories
2. It will go through each active repositories
3. It will query all branches in a repo
4. It will go through each branches in a repo and fetch all commits made in yesterday.
5. It will update commits accordingly to each member of notional - labs

### B. Issues and PRs query
1. It will query all public events in these organizations: notional-labs, osmosis-labs, cosmos, scrtlabs
2. It will filter all events related to notional-labs members and in yesterday
3. It will update issues and prs accordingly to each member of notional - labs

## Requirements
- python3.6+  

## How to install  
1. Run command below  
```bash
apt update \
&& apt install -y python3-pip python3-venv git tmux \
&& git clone https://github.com/notional-labs/helpful-tools.git \
&& cd helpful-tools/github-commits-monitoring-tool \
&& python3 -m venv venv \
&& source venv/bin/activate \
&& pip3 install -r requirements.txt
```
2. [Create Discord token](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
3. Fill in config.ini  
4. Invite the bot to your channel

## How to run  
Start monitoring bot
```
tmux new -s discord_monitor_bot -d cd ~/helpful-tools/github-commits-monitoring-tool && source venv/bin/activate && python3 discord_bot.py
```  
  
### Alternatively, the bot can be run through systemd:  
- If necessary, change the username and the path to the script folder in `discord-bot-monitor-github.service`

- Start the service  
```
ln -s $HOME/helpful-tools/github-commits-monitoring-tool/discord-bot-monitor-github.service /etc/systemd/system/ \
&& systemctl daemon-reload \
&& systemctl enable discord-bot-monitor-github.service \
&& systemctl start discord-bot-monitor-github.service \
&& systemctl status discord-bot-monitor-github.service
```  
