from tinydb import TinyDB
from instagramAPI import getLatestIGPosts, checkInstagramUser
from twitterAPI import getLatestTweets, checkTwitterUser
from discord.ext import commands, tasks
import discord
import datetime

import logging
import time
import os
from dotenv import load_dotenv
import re
load_dotenv()

# Setup database
db = TinyDB('database.json')
def doc(): return db.get(doc_id=1)
def updateDoc(obj): db.update(obj, doc_ids=[1])


if not doc():
    db.insert({"instagram": [], "twitter": []})

# discord bot commands
bot = commands.Bot(command_prefix='s!')

# Input the Discord Information
channelID = 452286672441442355


@bot.event
async def on_ready():
    # printing out message so it looks cool
    print(f'{bot.user.name} has connected to Discord!')


@tasks.loop(minutes=1.0)  # repeat every ...
async def myLoop():
    await bot.wait_until_ready()

    channel = bot.get_channel(channelID)

    prevTime = doc().get("prevTime")

    if prevTime:
        for user in doc()["instagram"]:
            for p in getLatestIGPosts(user, prevTime):
                embed = discord.Embed(
                    description=p["post_text"], color=13453419, timestamp=datetime.datetime.utcfromtimestamp(p["post_timestamp"]))
                embed.set_author(
                    name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                embed.set_footer(
                    text="Instagram", icon_url="https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png")

                embed.set_image(url=p["post_media_URL"])

                await channel.send(content=f"**New post from {user}**\n{p['post_URL']}\n{'Click to view video' if p['post_isVideo'] else ''}", embed=embed)

        for user in doc()["twitter"]:
            for p in getLatestTweets(user, prevTime):
                embed = discord.Embed(
                    description=p["post_text"], color=44270, timestamp=datetime.datetime.utcfromtimestamp(p["post_timestamp"]))
                embed.set_author(
                    name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                embed.set_footer(
                    text="Twitter", icon_url="https://cdn.cms-twdigitalassets.com/content/dam/developer-twitter/images/Twitter_logo_blue_48.png")

                if p.get("post_media_URL"):
                    embed.set_image(url=p["post_media_URL"])

                await channel.send(content=f"**New tweet from @{user}**\n{p['post_URL']}\n{'Click to view video' if p['post_isVideo'] else ''}", embed=embed)

    updateDoc({"prevTime": time.time()})


# ping will respond pong to ensure that the bot is alive
@bot.command()
async def ping(ctx):
    await ctx.send('Pong')


# @bot.command()
# async def setchannel(ctx, *args):
#     channelID = args[0]
#     channel = bot.get_channel(channelID)
#     print(channel)

@ bot.command()
async def add(ctx, *args):
    # ensuring there is at least one argument/help command
    if len(args) != 2:
        await ctx.send("You need to enter `s!add {social-media-site} {username}`")
        return

    # checking the first argument (platform management)
    socialMedia = args[0].lower()
    if socialMedia != "twitter" and socialMedia != "instagram":
        await ctx.send("Invalid social media site entered. Available social media platforms are `twitter` and `instagram`.")
        return

    platform = socialMedia.capitalize()

    # looks at new user
    newUser = " ".join(args[1:])

    # checks if user account doesn't exist
    if not globals()[f"check{platform}User"](newUser):
        await ctx.send(f"`{newUser}` does not exist on {platform}.")
        return

    # checks if user exists already
    if newUser in doc()[socialMedia]:
        await ctx.send(f"Updates from `{newUser}` already exist.")
        return

    db.update({socialMedia: [*doc()[socialMedia], newUser]}, doc_ids=[1])
    await ctx.send(f"Updates from `{newUser}` on `{platform}` will be posted.")


@ bot.command()
async def remove(ctx, *args):
    if len(args) != 2:
        await ctx.send("You need to enter `s!add {social-media-site} {username}`.")
        return

    # checking the first argument (platform management)
    socialMedia = args[0].lower()
    if socialMedia != "twitter" and socialMedia != "instagram":
        await ctx.send("Invalid social media site entered. Available social media platforms are `twitter` and `instagram`.")
        return

    platform = socialMedia.capitalize()

    # looks to see if user even exists
    newUser = " ".join(args[1:])
    if not newUser in doc()[socialMedia]:
        await ctx.send(f"Updates from `{newUser}` don't exist.")
        return

    deleteUserindex = doc()[socialMedia].index(newUser)
    updatedUsers = doc()[socialMedia]
    updatedUsers.pop(deleteUserindex)
    db.update({socialMedia: [updatedUsers]}, doc_ids=[1])

    await ctx.send(f"Posts from `{newUser}` on `{platform}` will no longer be posted.")


@ bot.command()
async def list(ctx):
    await ctx.send('Your Instagram Accounts:' + re.sub("[\[\]']", '', str(doc()['instagram'])) +
                   '\n' + 'Your Twitter Accounts:' + re.sub("[\[\]']", '', str(doc()['twitter'])))

    instagramEmbed = discord.Embed(
        title="Instagram Accounts", description=str('\n'.join(doc()['instagram'])), color=13453419)
    twitterEmbed = discord.Embed(
        title="Twitter Accounts", description=str('\n'.join(doc()['twitter'])), color=44270)

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
