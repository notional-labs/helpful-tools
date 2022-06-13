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
disc_log.setLevel(logging.DEBUG)

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
    memberContributions = github_monitor.queryContributions()
    compareView = data_output.compareView(memberContributions)
    detailView = data_output.detailView(memberContributions)

    message_time = data_output.time_print()
    message = "THIS IS YESTERDAY REPORT\n{}\n---------------------\n\n{}\n\n{}".format(message_time, compareView, detailView)
    

    message_packets = message.split("\n\n")
    print(message_packets)
    print("=== DONE REPORT ===")

    return message_packets

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
    message_packets = await executor(monitor_logic)
    for packet in message_packets:
        if packet == "":
            continue
        await message_channel.send(packet)

@report_output.before_loop
async def before_report_output():
    for _ in range(60*60*24):  # loop the whole day
        if datetime.datetime.now().hour == 7 and datetime.datetime.now().minute == 37:  # 24 hour format, CEST time
            print("getting github info")
            return
        await asyncio.sleep(1)# wait a second before looping again. You can make it more 

bot.run(TOKEN)