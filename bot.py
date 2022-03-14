from instagramAPI import latestIGPost
from twitterAPI import latestTweet
import discord
from discord.ext import tasks, commands

import logging
import os
from dotenv import load_dotenv
load_dotenv()

# Input the account names you want
usernameIG = "edisonfang123"
usernameTwitter = "EricisonF"

# input the discord information
serverName = "egg simps ᕕ( ᐛ )ᕗ"
channelID = 952684854917607458

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
    guild = discord.utils.get(client.guilds, name=serverName)
    channel = guild.get_channel(channelID)
    await channel.send(data["link"])


@tasks.loop(seconds=10)  # repeat after every 10 seconds
async def myLoop():
    # instagram part
    latestIGPostData = latestIGPost(usernameIG)
    latestIGPostDataLink = latestIGPostData["link"]

    if(allPosts[0] != latestIGPostDataLink + '\n'):
        await embeddedLink(latestIGPostData)
        allPosts[0] = latestIGPostDataLink + '\n'
        previousPosts.seek(0)
        previousPosts.writelines(allPosts)
        previousPosts.truncate()

    # twitter part
    latestTweetData = latestTweet(usernameTwitter)
    latestTweetDataLink = latestTweetData["link"]

    if(allPosts[1] != latestTweetDataLink):
        await embeddedLink(latestTweetData)
        allPosts[1] = latestTweetDataLink
        previousPosts.seek(0)
        previousPosts.writelines(allPosts)
        previousPosts.truncate()

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
