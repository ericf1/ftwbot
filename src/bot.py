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
        "icon": "https://cdn.cms-twdigitalassets.com/content/dam/developer-twitter/images/Twitter_logo_blue_`48.png",
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


@tasks.loop(minutes=1.0)  # repeat every ...
async def myLoop():
    await bot.wait_until_ready()
    await update()


# ping will respond pong to ensure that the bot is alive
@ bot.command()
async def ping(ctx):
    await ctx.send('Pong')


@ bot.command()
async def setChannel(ctx, channel: discord.TextChannel = None):
    if not await hasPerms(ctx):
        return

    if channel:
        updateDoc(ctx.guild.id, {"channelID": channel.id})
    else:
        updateDoc(ctx.guild.id, {"channelID": ctx.channel.id})

    await addReaction(ctx)


@ setChannel.error
async def setChannel_error(ctx, error):
    if isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!setChannel #{text-channel}`")


@bot.command()
async def update(ctx=None):
    for serverID in db.tables():

        if not doc(serverID).get("channelID"):
            return

        channel = bot.get_channel(doc(serverID)["channelID"])
        prevTime = doc(serverID).get("prevTime")

        if prevTime:
            for socialMedia in socialsData.keys():
                platform = socialMedia.capitalize()
                for user in doc(serverID)["socials"][socialMedia]:
                    posts = globals()[f"getLatest{platform}Posts"](
                        user, prevTime)
                    if posts:
                        for p in posts:
                            embed = discord.Embed(
                                description=p["post_text"], color=socialsData[socialMedia]["color"], timestamp=datetime.utcfromtimestamp(p["post_timestamp"]).replace(tzinfo=timezone.utc))
                            embed.set_author(
                                name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                            embed.set_footer(
                                text=platform, icon_url=socialsData[socialMedia]["icon"])

                            if p.get("post_media_URL"):
                                embed.set_image(url=p["post_media_URL"])

                            await channel.send(content=f"**New post from {user} on {platform}**\n{p['post_URL']}\n{'Click to view video' if p.get('post_isVideo') else ''}", embed=embed)

        updateDoc(serverID, {"prevTime": int(time.time())})

    if ctx:
        await addReaction(ctx)


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


# Wilson's logging thing
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

myLoop.start()
bot.run(os.getenv('DISCORD_TOKEN'))
