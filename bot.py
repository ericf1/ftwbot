from turtle import goto, title
from tinydb import TinyDB
from instagramAPI import getLatestIGPosts
from twitterAPI import getLatestTweets
from discord.ext import tasks, commands
import discord

import logging
import time
import os
from dotenv import load_dotenv
load_dotenv()

# Input the account names you want
# instagram = ["edisonfang123", "mindset_dive"]
# twitter = ["EricisonF", "mindset_dive", "briannam10"]
# maxAccounts = len(instagram) + len(twitter)

# Setup database
db = TinyDB('database.json')
def doc(): return db.get(doc_id=1)


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


# @tasks.loop(minutes=1)  # repeat every ...
async def myLoop():
    await bot.wait_until_ready()

    channel = bot.get_channel(channelID)

    prevTime = doc().get("prevTime")

    if prevTime:
        for user in doc()["instagram"]:
            for p in getLatestIGPosts(user, prevTime):
                embed = discord.Embed(
                    description=p["post_text"], color=13453419, timestamp=p["post_timestamp"])
                embed.set_author(
                    name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                embed.set_footer(
                    text="Instagram", icon_url="https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png")

                embed.set_image(url=p["post_media_URL"])

                await channel.send(content=f"**New post from {user}**\n{p['post_URL']}\n{'Click to view video' if p['post_isVideo'] else ''}", embed=embed)

        for user in doc()["twitter"]:
            for p in getLatestTweets(user, prevTime):
                embed = discord.Embed(
                    description=p["post_text"], color=44270, timestamp=p["post_timestamp"])
                embed.set_author(
                    name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                embed.set_footer(
                    text="Twitter", icon_url="https://cdn.cms-twdigitalassets.com/content/dam/developer-twitter/images/Twitter_logo_blue_48.png")

                if p.get("post_media_URL"):
                    embed.set_image(url=p["post_media_URL"])

                await channel.send(content=f"**New tweet from @{user}**\n{p['post_URL']}\n{'Click to view video' if p['post_isVideo'] else ''}", embed=embed)

    db.update({"prevTime": time.time()}, doc_ids=[1])


# ping will respond pong to ensure that the bot is alive
@bot.command()
async def ping(ctx):
    await ctx.send('Pong')


@bot.command()
async def add(ctx, *args):
    if len(args) != 2:
        await ctx.send("You need to enter `s!add {social-media-site} {username}`")
        return

    socialMedia = args[0].lower()

    if socialMedia != "twitter" and socialMedia != "instagram":
        await ctx.send("Invalid social media site entered. Available social media platforms are `twitter` and `instagram`.")
        return

    # to ensure there are no duplicates of user accounts
    try:
        doc()[socialMedia].index(args[1])
        await ctx.send(f"Updates from `{args[1]}` already exist.")
    except:
        db.update({f"{args[0]}": [*doc()[socialMedia], args[1]]}, doc_ids=[1])
        await ctx.send(f"Updates from `{args[1]}` on `{args[0]}` will be posted.")


# Wilson's logging thing
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# myLoop.start()
bot.run(os.getenv('DISCORD_TOKEN'))
