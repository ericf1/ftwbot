from turtle import update
from tinydb import TinyDB
from instagramAPI import getLatestIGPosts, checkInstagramUser
from twitterAPI import getLatestTweets, checkTwitterUser
from discord.ext import commands, tasks
import discord

import logging
import time
import os
from dotenv import load_dotenv
load_dotenv()

socialsData = {
    "instagram": {
        "icon": "https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png",
        "color": 13453419
    },
    "twitter": {
        "icon": "https://cdn.cms-twdigitalassets.com/content/dam/developer-twitter/images/Twitter_logo_blue_48.png",
        "color": 44270
    }
}

# Setup database
db = TinyDB('database.json')


def doc(server_id):
    table = db.table(str(server_id))

    if not table.get(doc_id=1):
        socialMediaObject = {}

        for socialMedia in socialsData.keys():
            socialMediaObject[socialMedia] = []

        table.insert({"socials": socialMediaObject})

    return table.get(doc_id=1)


def updateDoc(server_id, obj):
    table = db.table(str(server_id))

    if not table.get(doc_id=1):
        socialMediaObject = {}

        for socialMedia in socialsData.keys():
            socialMediaObject[socialMedia] = []

        table.insert({"socials": socialMediaObject})

    table.update(obj, doc_ids=[1])


# discord bot commands
bot = commands.Bot(command_prefix='s!')


async def isAdmin(ctx):
    """ isAdmin = ctx.author.permissions_in(ctx.channel).administrator
    if not isAdmin:
        await ctx.send("You do not have permission to use this command.")
    return isAdmin """

    return True


def to_lower(arg): return arg.lower()


@bot.event
async def on_ready():
    # printing out message so it looks cool
    print(f'{bot.user.name} has connected to Discord!')


@tasks.loop(minutes=1.0)  # repeat every ...
async def myLoop():
    await bot.wait_until_ready()

    for serverID in db.tables():
        if not doc(serverID).get("channelID"):
            return

        channel = bot.get_channel(doc(serverID)["channelID"])
        prevTime = doc(serverID).get("prevTime")

        if prevTime:
            for user in doc(serverID)["socials"]["instagram"]:
                posts = getLatestIGPosts(user, prevTime)
                if posts:
                    for p in posts:
                        embed = discord.Embed(
                            description=p["post_text"], color=socialsData["instagram"]["color"], timestamp=p["post_timestamp"])
                        embed.set_author(
                            name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                        embed.set_footer(
                            text="Instagram", icon_url=socialsData["instagram"]["icon"])

                        embed.set_image(url=p["post_media_URL"])

                        await channel.send(content=f"**New post from {user}**\n{p['post_URL']}\n{'Click to view video' if p['post_isVideo'] else ''}", embed=embed)

            for user in doc(serverID)["socials"]["twitter"]:
                tweets = getLatestTweets(user, prevTime)
                if tweets:
                    for p in tweets:
                        embed = discord.Embed(
                            description=p["post_text"], color=socialsData["twitter"]["color"], timestamp=p["post_timestamp"])
                        embed.set_author(
                            name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                        embed.set_footer(
                            text="Twitter", icon_url=socialsData["twitter"]["icon"])

                        if p.get("post_media_URL"):
                            embed.set_image(url=p["post_media_URL"])

                        await channel.send(content=f"**New tweet from @{user}**\n{p['post_URL']}\n{'Click to view video' if p.get('post_isVideo') else ''}", embed=embed)

        updateDoc(serverID, {"prevTime": int(time.time())})


# ping will respond pong to ensure that the bot is alive
@bot.command()
async def ping(ctx):
    await ctx.send('Pong')


@bot.command()
async def setChannel(ctx, channel: discord.TextChannel = None):
    if not await isAdmin(ctx):
        return

    if channel:
        updateDoc(ctx.guild.id, {"channelID": channel.id})
    else:
        updateDoc(ctx.guild.id, {"channelID": ctx.channel.id})
    await ctx.message.add_reaction("✅")


@setChannel.error
async def setChannel_error(ctx, error):
    if isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!setChannel #{text-channel}`")


@bot.command()
async def add(ctx, socialMedia: to_lower, user: str):
    if not await isAdmin(ctx):
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
    await ctx.message.add_reaction("✅")


@add.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!add {social-media-site} {username}`")


@bot.command()
async def remove(ctx, socialMedia: to_lower, user: str):
    if not await isAdmin(ctx):
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
    await ctx.message.add_reaction("✅")


@remove.error
async def remove_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!remove {social-media-site} {username}`")


@bot.command()
async def list(ctx):
    if not await isAdmin(ctx):
        return

    instagramEmbed = discord.Embed(
        title="Accounts", description='\n'.join(doc(ctx.guild.id)["socials"]['instagram']), color=socialsData["instagram"]["color"])
    instagramEmbed.set_footer(
        text="Instagram", icon_url=socialsData["instagram"]["icon"])

    twitterEmbed = discord.Embed(
        title="Accounts", description='\n'.join(doc(ctx.guild.id)["socials"]['twitter']), color=socialsData["twitter"]["color"])
    twitterEmbed.set_footer(
        text="Twitter", icon_url=socialsData["twitter"]["icon"])

    await ctx.send(embed=instagramEmbed)
    await ctx.send(embed=twitterEmbed)


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
