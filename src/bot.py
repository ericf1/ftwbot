from datetime import datetime, timezone
from multiprocessing.sharedctypes import Value
import time
from _social_data import SOCIALS_DATA

from dotenv import load_dotenv
import requests
import os
import sys

from discord.ext import commands, tasks
import discord

from database.ChannelsDatabase import ChannelsDatabase
from database.SocialDatabase import SocialDatabase
from database.TimeDatabase import TimeDatabase
from database.SettingsDatabase import SettingsDatabase


# Necessary functional commands
load_dotenv()
social_database = SocialDatabase(0)
time_database = TimeDatabase(1)
settings_database = SettingsDatabase(2)
channels_database = ChannelsDatabase(3)

SERVER_API = os.getenv("API_SERVER")
bot = commands.Bot(command_prefix='s!', case_insensitive=True)
http = requests.Session()

# Helper functions


async def has_perms(ctx):
    has_perms = ctx.author.permissions_in(ctx.channel).manage_channels
    if not has_perms:
        await ctx.send("You do not have permission to use this command.")
    return has_perms


async def add_reaction(ctx): await ctx.message.add_reaction("✅")


def to_lower(arg): return arg.lower()


# formatter function that sends the correct social media post
async def formatter(user, prev_time, social_media, channel):
    platform = social_media.capitalize()
    posts = await globals()[f"getLatest{platform}Posts"](user, prev_time)
    print(posts)
    if posts == None:
        return
    for p in posts:
        embed = discord.Embed(
            description=p["post_text"], color=SOCIALS_DATA[social_media]["color"], timestamp=datetime.utcfromtimestamp(p["post_timestamp"]).replace(tzinfo=timezone.utc))
        embed.set_author(
            name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
        embed.set_footer(
            text=platform, icon_url=SOCIALS_DATA[social_media]["icon"])

        if p.get("post_media_URL"):
            embed.set_image(url=p["post_media_URL"])
        await channel.send(
            content=f"**New post from {user} on {platform}**\n{p['post_URL']}\n{'Click to view video' if p.get('post_isVideo') else ''}", embed=embed)


@ bot.event
async def on_ready():
    # printing out message so it looks cool
    print(f'{bot.user.name} has connected to Discord!')


# ping will respond pong to ensure that the bot is alive
@ bot.command()
async def ping(ctx):
    await ctx.send('Pong')
    await add_reaction(ctx)


# Channel commands:
@ bot.command()
async def addChannel(ctx, channel: discord.TextChannel = None):
    if not await has_perms(ctx):
        return

    if channel:
        channels_database.add(ctx.guild.id, channel.id)
    else:
        channels_database.add(ctx.guild.id, ctx.channel.id)

    await add_reaction(ctx)


@ addChannel.error
async def addChannel_error(ctx, error):
    if isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!setChannel #{text-channel}`")


@ bot.command()
async def removeChannel(ctx, channel: discord.TextChannel = None):
    if not await has_perms(ctx):
        return

    channels_database.remove(ctx.guild.id, channel.id)

    await add_reaction(ctx)


@ removeChannel.error
async def removeChannel_error(ctx, error):
    if isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!setChannel #{text-channel}`")


@ bot.command()
async def listChannel(ctx):
    if not await has_perms(ctx):
        return
    embed = discord.Embed(title="Channels", description='\n'.join(
        channels_database.get(ctx.guild.id)), color=1146986)

    embed.set_footer(text="Channels",
                     icon_url="pictures\icons8-restart.gif")
    await ctx.send(embed=embed)
    await add_reaction(ctx)


@ listChannel.error
async def listChannel_error(ctx, error):
    if isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!setChannel #{text-channel}`")


# Social Media Usernames:
@ bot.command()
async def add(ctx, social_media: to_lower, user: str):
    if not await has_perms(ctx):
        return

    # checking the first argument (platform management)
    if social_media not in SOCIALS_DATA.keys():
        await ctx.send(f"Invalid social media site entered. Available social media platforms are {', '.join(SOCIALS_DATA.keys())}.")
        return

    platform_capitalize = social_media.capitalize()
    # checks if user account doesn't exist
    url = f"{SERVER_API}/{social_media}-user"
    params = {'username': user}
    resp = http.get(url, params=params)

    if not resp.json().get("result"):
        await ctx.send(f"`User {user}` does not exist on {platform_capitalize}.")
        return

    social_database.add(ctx.guild.id, user)

    await add_reaction(ctx)


@ add.error
async def add_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!add {social-media-site} {username}`")
        return
    if isinstance(error, ValueError):
        await ctx.send("The user already exists in the list")
        return
    await ctx.send(repr(error))


@ bot.command()
async def remove(ctx, social_media: to_lower, user: str):
    if not await has_perms(ctx):
        return

    # checking the first argument (platform management)
    if social_media not in SOCIALS_DATA.keys():
        await ctx.send(f"Invalid social media site entered. Available social media platforms are {', '.join(SOCIALS_DATA.keys())}.")
        return

    social_database.remove(ctx.guild.id, user)

    await add_reaction(ctx)


@ remove.error
async def remove_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!remove {social-media-site} {username}`")
        return
    await ctx.send(repr(error))


@ bot.command()
async def list(ctx):
    if not await has_perms(ctx):
        return

    for social_media, v in SOCIALS_DATA.items():
        accounts = social_database.get(ctx.guild.id).get(social_media)
        if accounts is None:
            accounts = []
        embed = discord.Embed(
            title="Accounts", description='\n'.join(accounts), color=v["color"])
        embed.set_footer(text=social_media.capitalize(),
                         icon_url=v["icon"])
        await ctx.send(embed=embed)

    await add_reaction(ctx)


@ list.error
async def list_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!remove {social-media-site} {username}`")
        return
    await ctx.send(repr(error))


@ tasks.loop(seconds=1.0)  # repeat every 10 minutes
async def main_loop():
    await bot.wait_until_ready()
    for server_id in social_database.all:
        prev_time = time_database.get(server_id)
        socials = social_database.get(server_id)
        channels = channels_database.get(server_id)
        if channels is None or channels is []:
            continue
        for channel_id in channels:
            channel = bot.get_channel(int(channel_id))
            if(channel == None):
                continue
            for socialMedia in socialsData.keys():
                for user in socials[socialMedia]:
                params = [user, prevTime, socialMedia, channel]
                threadsFunctions.append(params)
        updateDoc(serverID, {"prevTime": int(time.time())})
        try:
            await formatter(params[0], params[1], params[2], params[3])
        except Exception as e:
            print(repr(e))


def error_func():
    raise ValueError("AHHAA")


if __name__ == '__main__':
    # main_loop.start()
    # bot.run(os.getenv('DISCORD_TOKEN'))
    pass
