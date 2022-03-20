from tinydb import TinyDB, Query
from instagramAPI import getLatestIGPosts
from twitterAPI import getLatestTweets
from discord.ext import tasks, commands

import logging
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Input the account names you want
instagram = ["edisonfang123", "mindset_dive"]
twitter = ["EricisonF", "mindset_dive", "briannam10"]
maxAccounts = len(instagram) + len(twitter)

# Setup database
db = TinyDB('database.json')
if not db.get(doc_id=1):
    db.insert({"twitter": [], "instagram": []})


# input the discord information
serverName = "egg simps ᕕ( ᐛ )ᕗ"
channelID = 452286672441442355

# discord client commands
client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    # printing out message so it looks cool
    print(f'{client.user.name} has connected to Discord!')


""" async def embeddedLink(data):
    channel = client.get_channel(channelID)
    prevTime = db.get(doc_id=1)["prevTime"]

    if prevTime:
        for username in db.get(doc_id=1)["twitter"]:
            tweets = getLatestTweets(username, prevTime)

        for username in db.get(doc_id=1)["instagram"]:
            posts = getLatestIGPosts(username, prevTime)

    db.update({"prevTime": time.time()}, doc_ids=[1]) """


@ tasks.loop(seconds=5)  # repeat after every 5 seconds
async def myLoop():
    await client.wait_until_ready()


# .ping will respond pong to ensure that the bot is alive
@ client.command()
async def ping(ctx):
    await ctx.send('Pong')


@ client.command()
async def test(ctx):
    await ctx.send("Ping")

# Wilson's logging thing
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

myLoop.start()
client.run(os.getenv('DISCORD_TOKEN'))
