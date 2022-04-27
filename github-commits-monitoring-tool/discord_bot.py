import logging
import sys
import configparser
import discord
from discord.ext import commands, tasks
import github_monitor.github_monitor as github_monitor
import data_output
import datetime
import asyncio
import typing # For typehinting 
import functools

# Turn Down Discord Logging
disc_log = logging.getLogger('discord')
disc_log.setLevel(logging.INFO)

# Configure Logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logger = logging.getLogger(__name__)

# Load config
c = configparser.ConfigParser()
c.read("config.ini", encoding='utf-8')

TOKEN              = str(c["DISCORD"]["discord_bot_token"])
LISTENING_CHANNEL = int(c["DISCORD"]["channel_to_listen"])

client = discord.Client()
bot = commands.Bot("$")

def monitor_logic():
    member_contributions = github_monitor.query_member_contributions()
    message = data_output.pretty_print_details(member_contributions)
    message = data_output.time_print(message)
    print("=== DONE REPORT ===")

    return message

async def executor(blocking_func: typing.Callable):
    func = functools.partial(blocking_func)
    return await client.loop.run_in_executor(None, func)

@bot.event
async def on_ready():
    print("Logged in as {}".format(bot.user.name))
    print("------")
    report_output.start()

# report output to output all reports of dev work in a day
@tasks.loop(hours=24)
async def report_output():
    message_channel = bot.get_channel(LISTENING_CHANNEL)
    message = await executor(monitor_logic)
    await message_channel.send(message)

@report_output.before_loop
async def before_report_output():
    for _ in range(60*60*24):  # loop the whole day
        if datetime.datetime.now().minute == 53:  # 24 hour format
            print("getting github info")
            return
        await asyncio.sleep(1)# wait a second before looping again. You can make it more 

bot.run(TOKEN)