from turtle import update
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

instagramIcon = "https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png"
twitterIcon = "https://cdn.cms-twdigitalassets.com/content/dam/developer-twitter/images/Twitter_logo_blue_48.png"

# Setup database
db = TinyDB('database.json')
def doc(): return db.get(doc_id=1)
def updateDoc(obj): db.update(obj, doc_ids=[1])


if not doc():
    db.insert({"instagram": [], "twitter": []})

# discord bot commands
bot = commands.Bot(command_prefix='s!')


async def isAdmin(ctx):
    isAdmin = ctx.author.permissions_in(ctx.channel).administrator
    if not isAdmin:
        await ctx.send("You do not have permission to use this command.")
    return isAdmin


@bot.event
async def on_ready():
    # printing out message so it looks cool
    print(f'{bot.user.name} has connected to Discord!')


@tasks.loop(minutes=1.0)  # repeat every ...
async def myLoop():
    await bot.wait_until_ready()

    channel = bot.get_channel(doc()["channelID"])

    prevTime = doc().get("prevTime")

    if prevTime:
        for user in doc()["instagram"]:
            posts = getLatestIGPosts(user, prevTime)
            if posts:
                for p in posts:
                    embed = discord.Embed(
                        description=p["post_text"], color=13453419, timestamp=p["post_timestamp"])
                    embed.set_author(
                        name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                    embed.set_footer(
                        text="Instagram", icon_url=instagramIcon)

                    embed.set_image(url=p["post_media_URL"])

                    await channel.send(content=f"**New post from {user}**\n{p['post_URL']}\n{'Click to view video' if p['post_isVideo'] else ''}", embed=embed)

        for user in doc()["twitter"]:
            tweets = getLatestTweets(user, prevTime)
            if tweets:
                for p in tweets:
                    embed = discord.Embed(
                        description=p["post_text"], color=44270, timestamp=p["post_timestamp"])
                    embed.set_author(
                        name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                    embed.set_footer(
                        text="Twitter", icon_url=twitterIcon)

                    if p.get("post_media_URL"):
                        embed.set_image(url=p["post_media_URL"])

                    await channel.send(content=f"**New tweet from @{user}**\n{p['post_URL']}\n{'Click to view video' if p.get('post_isVideo') else ''}", embed=embed)

    updateDoc({"prevTime": int(time.time())})


# ping will respond pong to ensure that the bot is alive
@ bot.command()
async def ping(ctx):
    await ctx.send('Pong')


@ bot.command()
async def setChannel(ctx, id: int = None):
    if not await isAdmin(ctx):
        return

    if id:
        if ctx.guild.get_channel(id):
            updateDoc({"channelID": id})
        else:
            await ctx.send(f"That channel doesn't exist in this server.")
            return
    else:
        updateDoc({"channelID": ctx.channel.id})

    await ctx.send(f"Updates will be posted in <#{doc()['channelID']}>.")


@ bot.command()
async def add(ctx, *args):
    if not await isAdmin(ctx):
        return

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

    user = args[1]
    # checks if user account doesn't exist
    if not globals()[f"check{platform}User"](user):
        await ctx.send(f"`{user}` does not exist on {platform}.")
        return

    # checks if user exists in database already
    if user in doc()[socialMedia]:
        await ctx.send(f"Updates from `{user}` already exist.")
        return

    updateDoc({socialMedia: [*doc()[socialMedia], user]})
    await ctx.send(f"Updates from `{user}` on `{platform}` will be posted.")


@ bot.command()
async def remove(ctx, *args):
    if not await isAdmin(ctx):
        return

    if len(args) != 2:
        await ctx.send("You need to enter `s!remove {social-media-site} {username}`.")
        return

    # checking the first argument (platform management)
    socialMedia = args[0].lower()
    if socialMedia != "twitter" and socialMedia != "instagram":
        await ctx.send("Invalid social media site entered. Available social media platforms are `twitter` and `instagram`.")
        return

    platform = socialMedia.capitalize()

    # checks if user exists in database
    user = args[1]
    if not user in doc()[socialMedia]:
        await ctx.send(f"Updates from `{user}` don't exist.")
        return

    users = doc()[socialMedia]
    users.pop(users.index(user))

    updateDoc({socialMedia: users})

    await ctx.send(f"Posts from `{user}` on `{platform}` will no longer be posted.")


@ bot.command()
async def list(ctx):
    if not await isAdmin(ctx):
        return

    instagramEmbed = discord.Embed(
        title="Accounts", description='\n'.join(doc()['instagram']), color=13453419)
    instagramEmbed.set_footer(text="Instagram", icon_url=instagramIcon)

    twitterEmbed = discord.Embed(
        title="Accounts", description='\n'.join(doc()['twitter']), color=44270)
    twitterEmbed.set_footer(text="Twitter", icon_url=twitterIcon)

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
