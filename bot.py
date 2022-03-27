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
load_dotenv()

instagramIcon = "https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png"
twitterIcon = "https://cdn.cms-twdigitalassets.com/content/dam/developer-twitter/images/Twitter_logo_blue_48.png"

# Setup database
db = TinyDB('database.json')
db2 = TinyDB('servers.json')


def doc(id):
    return db.get(doc_id=id)


def docServer(): return list(db2.get(doc_id=1).values())[0]
def updateDoc(obj, id): db.update(obj, doc_ids=[id])


def addServer(server): db2.update(
    {'servers': [*docServer()['servers'], server]}, doc_ids=[1])


if not db2.get(doc_id=1):
    db2.insert({'servers': []})
for id in range(len(docServer())):
    id = id + 1
    if not doc(id):
        db.insert({"instagram": [], "twitter": []})
# discord bot commands
bot = commands.Bot(command_prefix='s!')


async def isAdmin(ctx):
    if not ctx.author.permissions_in(ctx.channel).administrator:
        await ctx.send("You do not have permission to use this command.")
    return ctx.author.permissions_in(ctx.channel).administrator


@ bot.event
async def on_ready():
    # printing out message so it looks cool
    print(f'{bot.user.name} has connected to Discord!')


@ bot.event
async def on_guild_join(guild):
    print(guild.id)
    # addServer(str(guild))


@ tasks.loop(minutes=1.0)  # repeat every ...
async def myLoop():
    await bot.wait_until_ready()
    if not doc(1):
        return
    for dbid in range(len(db)):
        dbid = dbid + 1

        if not doc(dbid).get("channelID"):
            continue

        channel = bot.get_channel(doc(dbid).get("channelID"))

        prevTime = doc(dbid).get("prevTime")

        if prevTime:
            for user in doc(dbid).get("instagram"):
                for p in getLatestIGPosts(user, prevTime):
                    embed = discord.Embed(
                        description=p["post_text"], color=13453419, timestamp=datetime.datetime.utcfromtimestamp(p["post_timestamp"]))
                    embed.set_author(
                        name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                    embed.set_footer(
                        text="Instagram", icon_url=instagramIcon)

                    embed.set_image(url=p["post_media_URL"])

                    await channel.send(content=f"**New post from {user}**\n{p['post_URL']}\n{'Click to view video' if p['post_isVideo'] else ''}", embed=embed)

            for user in doc(dbid).get("twitter"):
                for p in getLatestTweets(user, prevTime):
                    embed = discord.Embed(
                        description=p["post_text"], color=44270, timestamp=datetime.datetime.utcfromtimestamp(p["post_timestamp"]))
                    embed.set_author(
                        name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                    embed.set_footer(
                        text="Twitter", icon_url=twitterIcon)

                    if p.get("post_media_URL"):
                        embed.set_image(url=p["post_media_URL"])

                    await channel.send(content=f"**New tweet from @{user}**\n{p['post_URL']}\n{'Click to view video' if p['post_isVideo'] else ''}", embed=embed)

        updateDoc({"prevTime": time.time()}, dbid)


# ping will respond pong to ensure that the bot is alive
@ bot.command()
async def ping(ctx):
    await ctx.send('Pong')


@ bot.command()
async def setChannel(ctx, id: int = None):
    curGuild = ctx.guild
    docid = docServer().index(curGuild) + 1
    if not await isAdmin(ctx):
        return

    if id:
        if ctx.guild.get_channel(id):
            updateDoc({"channelID": id}, docid)
        else:
            await ctx.send(f"That channel doesn't exist in this server.")
            return
    else:
        updateDoc({"channelID": ctx.channel.id}, docid)

    await ctx.send(f"Updates will be posted in <#{doc(docid)['channelID']}>.")


@ bot.command()
async def add(ctx, *args):
    if not await isAdmin(ctx):
        return
    curGuild = ctx.guild
    docid = docServer().index(curGuild) + 1

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
    if newUser in doc(docid)[socialMedia]:
        await ctx.send(f"Updates from `{newUser}` already exist.")
        return

    updateDoc({socialMedia: [*doc(docid)[socialMedia], newUser]}, docid)
    await ctx.send(f"Updates from `{newUser}` on `{platform}` will be posted.")


@ bot.command()
async def remove(ctx, *args):
    if not await isAdmin(ctx):
        return

    if len(args) != 2:
        await ctx.send("You need to enter `s!add {social-media-site} {username}`.")
        return

    curGuild = ctx.guild
    docid = docServer().index(curGuild) + 1
    # checking the first argument (platform management)
    socialMedia = args[0].lower()
    if socialMedia != "twitter" and socialMedia != "instagram":
        await ctx.send("Invalid social media site entered. Available social media platforms are `twitter` and `instagram`.")
        return

    platform = socialMedia.capitalize()

    # looks to see if user even exists
    newUser = " ".join(args[1:])
    if not newUser in doc(docid)[socialMedia]:
        await ctx.send(f"Updates from `{newUser}` don't exist.")
        return

    deleteUserindex = doc(docid)[socialMedia].index(newUser)
    updatedUsers = doc(docid)[socialMedia].pop(deleteUserindex)
    updateDoc({socialMedia: [updatedUsers]}, docid)

    await ctx.send(f"Posts from `{newUser}` on `{platform}` will no longer be posted.")


@ bot.command()
async def list(ctx):
    if not await isAdmin(ctx):
        return
    curGuild = ctx.guild
    docid = docServer().index(curGuild) + 1

    instagramEmbed = discord.Embed(
        title="Instagram Accounts", description='\n'.join(doc(docid)['instagram']), color=13453419)
    instagramEmbed.set_footer(text="Instagram", icon_url=instagramIcon)

    twitterEmbed = discord.Embed(
        title="Twitter Accounts", description='\n'.join(doc(docid)['twitter']), color=44270)
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
