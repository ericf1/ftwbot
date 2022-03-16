from instagramAPI import getLatestIGPosts
from twitterAPI import getLatestTweets
from discord.ext import tasks, commands

import logging
import os
from dotenv import load_dotenv
load_dotenv()

# Input the account names you want
instagram = ["edisonfang123", "mindset_dive"]
twitter = ["EricisonF", "mindset_dive", "briannam10"]
maxAccounts = len(instagram) + len(twitter)

# input the discord information
serverName = "egg simps ᕕ( ᐛ )ᕗ"
channelID = 452286672441442355

# discord client commands
client = commands.Bot(command_prefix='.')

# opens the file that holds the data of the previous posts
previousPosts = open("posts.txt", "r+")
allPosts = previousPosts.readlines()

# to ensure that the bot is actually running


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

# printing out message so it looks cool


async def embeddedLink(data):
    channel = client.get_channel(channelID)
    if data["link"]:
        await channel.send(data["link"])

# abstraction for the latest post
# @params:
# username is username of user
# platform is IGPost or Tweet
# i is the counter for the file line


async def latestPost(username, platform, i):
    latestData = eval(f"latest{platform}('{username}')")
    latestDataLink = latestData["link"]

    print(username, platform, i)
    print(latestData, latestDataLink)

    if(i != maxAccounts - 1):
        latestDataLink += '\n'

    if(allPosts[i] != latestDataLink):
        await embeddedLink(latestData)
        allPosts[i] = latestDataLink
        previousPosts.seek(0)
        previousPosts.writelines(allPosts)
        previousPosts.truncate()


@tasks.loop(seconds=5)  # repeat after every 5 seconds
async def myLoop():
    await client.wait_until_ready()
    await latestPost(instagram[0], "IGPosts", 0)
    await latestPost(instagram[1], "IGPosts", 1)
    await latestPost(twitter[0], "Tweets", 2)
    await latestPost(twitter[1], "Tweets", 3)
    await latestPost(twitter[2], "Tweets", 4)

# .ping will respond pong to ensure that the bot is alive


@client.command()
async def ping(ctx):
    await ctx.send('Pong')

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
