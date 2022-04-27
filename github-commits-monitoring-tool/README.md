# chain-helpful-tools
This is a collection of helpful tools

# github-commits-monitoring-tool
Discord faucet bot for any blockchain based Cosmos

<details>
  <summary>List of available commands:</summary>

1. temp  
`$temp 1234`

</details>  


## Requirements
- python3.6+  

## How to install  
1. Run command below  
```bash
apt update \
&& apt install -y python3-pip python3-venv git tmux \
&& git clone https://github.com/notional-labs/cosmos-discord-faucet.git \
&& cd github-commits-monitoring-tool \
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
tmux new -s discord_monitor_bot -d cd ~/cosmos-discord-faucet && source venv/bin/activate && python3 discord_faucet_bot.py
```  
  
### Alternatively, the bot can be run through systemd:  
- If necessary, change the username and the path to the script folder in `discord-bot-monitor-github.service`  

- Start the service  
```
ln -s $HOME/cosmos-discord-faucet/discord-faucet-bot.service /etc/systemd/system/ \
&& systemctl daemon-reload \
&& systemctl enable discord-faucet-bot.service \
&& systemctl start discord-faucet-bot.service \
&& systemctl status discord-faucet-bot.service
```  
