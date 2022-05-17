from webbrowser import get
from dotenv import load_dotenv
import os
from turtle import update
from tinydb import TinyDB
from instagramAPI import getLatestInstagramPosts, checkInstagramUser
from twitterAPI import getLatestTwitterPosts, checkTwitterUser
from discord.ext import commands, tasks
import discord

import logging
import time
from datetime import datetime, timezone
load_dotenv()

socialsData = {
    "instagram": {
        "icon": "https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png",
        "color": 13453419
    },
    "twitter": {
        "icon": "https://abs.twimg.com/responsive-web/client-web/icon-ios.b1fc7275.png",
        "color": 44270
    }
}

# Setup database
db = TinyDB('database.json')


def doc(server_id):
    table = db.table(str(server_id))

    if not table.get(doc_id=1):
        table.insert({"socials": {}})

    for socialMedia in socialsData.keys():
        if socialMedia not in table.get(doc_id=1)["socials"].keys():
            socialMediaObject = table.get(doc_id=1)["socials"]
            socialMediaObject[socialMedia] = []

            table.update({"socials": socialMediaObject})

    return table.get(doc_id=1)


def updateDoc(server_id, obj):
    table = db.table(str(server_id))

    if not table.get(doc_id=1):
        table.insert({"socials": {}})

    for socialMedia in socialsData.keys():
        if socialMedia not in table.get(doc_id=1)["socials"].keys():
            socialMediaObject = table.get(doc_id=1)["socials"]
            socialMediaObject[socialMedia] = []

            table.update({"socials": socialMediaObject})

    table.update(obj, doc_ids=[1])

# formatter function that sends the correct social media post


async def formatter(user, prevTime, socialMedia, channel):
    platform = socialMedia.capitalize()
    posts = globals()[f"getLatest{platform}Posts"](user, prevTime)
    for p in posts:
        embed = discord.Embed(
            description=p["post_text"], color=socialsData[socialMedia]["color"], timestamp=datetime.utcfromtimestamp(p["post_timestamp"]).replace(tzinfo=timezone.utc))
        embed.set_author(
            name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
        embed.set_footer(
            text=platform, icon_url=socialsData[socialMedia]["icon"])

        if p.get("post_media_URL"):
            embed.set_image(url=p["post_media_URL"])

        await channel.send(
            content=f"**New post from {user} on {platform}**\n{p['post_URL']}\n{'Click to view video' if p.get('post_isVideo') else ''}", embed=embed)

# discord bot commands
bot = commands.Bot(command_prefix='s!')


async def hasPerms(ctx):
    hasPerms = ctx.author.permissions_in(ctx.channel).manage_channels
    if not hasPerms:
        await ctx.send("You do not have permission to use this command.")
    return hasPerms


async def addReaction(ctx): await ctx.message.add_reaction("✅")


def to_lower(arg): return arg.lower()


@bot.event
async def on_ready():
    # printing out message so it looks cool
    print(f'{bot.user.name} has connected to Discord!')


@tasks.loop(seconds=120.0)  # repeat every 120 seconds
async def mainLoop():
    await bot.wait_until_ready()
    threadsFunctions = []
    for serverID in db.tables():
        if(doc(serverID).get("prevTime") == None):
            updateDoc(serverID, {"prevTime": int(time.time())})
        channel = bot.get_channel(doc(serverID).get("channelID"))
        if(channel == None):
            continue
        prevTime = doc(serverID).get("prevTime")
        socials = doc(serverID).get("socials")
        for socialMedia in socialsData.keys():
            for user in socials[socialMedia]:
                params = [user, prevTime, socialMedia, channel]
                threadsFunctions.append(params)
        updateDoc(serverID, {"prevTime": int(time.time())})
    for params in threadsFunctions:
        await formatter(params[0], params[1], params[2], params[3])


# ping will respond pong to ensure that the bot is alive
@ bot.command()
async def ping(ctx):
    await ctx.send('Pong')
    await addReaction(ctx)


@ bot.command()
async def setChannel(ctx, channel: discord.TextChannel = None):
    if not await hasPerms(ctx):
        return

    if channel:
        updateDoc(ctx.guild.id, {"channelID": channel.id})
    else:
        updateDoc(ctx.guild.id, {"channelID": ctx.channel.id})

    if(doc(ctx.guild.id).get("prevTime") == None):
        updateDoc(ctx.guild.id, {"prevTime": int(time.time())})

    await addReaction(ctx)


@ setChannel.error
async def setChannel_error(ctx, error):
    if isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!setChannel #{text-channel}`")


@ bot.command()
async def add(ctx, socialMedia: to_lower, user: str):
    if not await hasPerms(ctx):
        return

    # checking the first argument (platform management)
    if socialMedia not in socialsData.keys():
        await ctx.send(f"Invalid social media site entered. Available social media platforms are {', '.join(socialsData.keys())}.")
        return

    platform = socialMedia.capitalize()
    # checks if user account doesn't exist
    if not globals()[f"check{platform}User"](user):
        await ctx.send(f"`User {user}` does not exist on {platform}.")
        return

    # checks if user exists in database already
    if user in doc(ctx.guild.id)["socials"][socialMedia]:
        await ctx.send(f"Updates from `{user}` already exist.")
        return

    socialsObj = doc(ctx.guild.id)["socials"]
    socialsObj[socialMedia] = [*socialsObj[socialMedia], user]

    updateDoc(ctx.guild.id, {"socials": socialsObj})

    await addReaction(ctx)


@ add.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!add {social-media-site} {username}`")


@ bot.command()
async def remove(ctx, socialMedia: to_lower, user: str):
    if not await hasPerms(ctx):
        return

    # checking the first argument (platform management)
    if socialMedia != "twitter" and socialMedia != "instagram":
        await ctx.send("Invalid social media site entered. Available social media platforms are `twitter` and `instagram`.")
        return

    # checks if user exists in database
    if not user in doc(ctx.guild.id)["socials"][socialMedia]:
        await ctx.send(f"Updates from `{user}` on {socialMedia} don't exist.")
        return

    users = doc(ctx.guild.id)["socials"][socialMedia]
    users.pop(users.index(user))

    socialsObj = doc(ctx.guild.id)["socials"]
    socialsObj[socialMedia] = users

    updateDoc(ctx.guild.id, {"socials": socialsObj})

    await addReaction(ctx)


@ remove.error
async def remove_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!remove {social-media-site} {username}`")


@ bot.command()
async def list(ctx):
    if not await hasPerms(ctx):
        return

    for socialMedia in socialsData:
        embed = discord.Embed(title="Accounts", description='\n'.join(doc(ctx.guild.id)[
            "socials"][socialMedia]), color=socialsData[socialMedia]["color"])
        embed.set_footer(text=socialMedia.capitalize(),
                         icon_url=socialsData[socialMedia]["icon"])
        await ctx.send(embed=embed)

    await addReaction(ctx)


# Discord Logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

mainLoop.start()

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))
