from dotenv import load_dotenv
import os
from turtle import update
from tinydb import TinyDB
from instagramAPI import getLatestInstagramPosts, checkInstagramUser
from twitterAPI import getLatestTwitterPosts, checkTwitterUser
from discord.ext import commands, tasks
import discord
import time
import asyncio
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
    posts = await globals()[f"getLatest{platform}Posts"](user, prevTime)
    print(posts)
    if(posts == None):
        return
    for p in posts:
        embed = discord.Embed(
            description=p["post_text"], color=socialsData[socialMedia]["color"], timestamp=datetime.utcfromtimestamp(p["post_timestamp"]).replace(tzinfo=timezone.utc))
        embed.set_author(
            name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
        embed.set_footer(
            text=platform, icon_url=socialsData[socialMedia]["icon"])

        if p.get("post_media_URL"):
            embed.set_image(url=p["post_media_URL"])
        try:
            await channel.send(
                content=f"**New post from {user} on {platform}**\n{p['post_URL']}\n{'Click to view video' if p.get('post_isVideo') else ''}", embed=embed)
        except Exception as e:
            print(repr(e))

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


@tasks.loop(seconds=30.0)  # repeat every 120 seconds
async def mainLoop():
    await bot.wait_until_ready()
    await update()


async def update():
    start = time.perf_counter()
    threadsFunctions = []
    for serverID in db.tables():
        prevTime = doc(serverID).get("prevTime")
        print(f"got this server with id: {serverID} and prevTime: {prevTime}")
        if(prevTime == None):
            updateDoc(serverID, {"prevTime": int(time.time())})
        if(doc(serverID).get("channelID") == None):
            print(f"{serverID} does not have a channel set")
            continue
        channel = bot.get_channel(doc(serverID).get("channelID"))
        channel = doc(serverID).get("channelID")
        if(channel == None):
            print(f"{serverID} is no longer connected")
            continue
        socials = doc(serverID).get("socials")
        for socialMedia in socialsData.keys():
            for user in socials[socialMedia]:
                threadsFunctions.append(asyncio.create_task(
                    formatter(user, prevTime, socialMedia, channel)))
        updateDoc(serverID, {"prevTime": int(time.time())})

    for threadsFunction in threadsFunctions:
        # time.sleep(1)
        await threadsFunction
    finish = time.perf_counter()
    print(f'finished in {round((finish-start)/60.0, 2)} minutes(s)')

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

mainLoop.start()

if __name__ == '__main__':
    bot.run(os.getenv('DISCORD_TOKEN'))
