import discord
from discord.ext import commands
import logging
import time
import os
import schedule
from dotenv import load_dotenv
load_dotenv()


""" from twitterAPI import latestTweet
from instagramAPI import latestIGPost """

# logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# variables
usernameIG = "thedivestudios"
usernameTwitter = ""

oldTweetLink = ""
oldIGLink = ""

# discord stuff
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

    guild = discord.utils.get(client.guilds, name="egg simps ᕕ( ᐛ )ᕗ")
    channel = guild.get_channel(452286672441442355)

    await channel.send("Connected!")

    while True:
        await channel.send("5 secs passed")
        time.sleep(5)


@client.event
async def on_message(msg):
    if msg.author == client.user:
        return

    if msg.content.lower()[:2] == "b!":
        if "ping" in msg.content.lower()[2:]:
            await msg.channel.send("Pong!")
        if "joke" in msg.content.lower()[2:]:
            await msg.channel.send("Your life is a joke!")


client.run(os.getenv('DISCORD_TOKEN'))


# discord - bot stuff

""" bot = commands.Bot(command_prefix='b!')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


@bot.command(name="ping")
async def pong(ctx):
    await ctx.send("pong")


bot.run(os.getenv('DISCORD_TOKEN')) """


# Loop to run continously check
""" while(True):
    time.sleep(60)
    if(usernameTwitter):
        latestTweetLink = latestTweet(usernameTwitter)
        if(oldTweetLink != latestTweetLink):
            embeddedLink(latestTweetLink)
            oldTweetLink = latestTweetLink

    if(usernameIG):
        latestIGLink = latestIGPost(usernameIG)
        if(oldIGLink != latestIGLink):
            embeddedLink(latestIGLink)
            oldIGLink = latestIGLink """
