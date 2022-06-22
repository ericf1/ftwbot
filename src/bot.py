from datetime import datetime, timezone
import time
from _social_data import SOCIALS_DATA
import aiohttp

from dotenv import load_dotenv
import requests
import os

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
testing = False
TESTING_CHANNEL = os.getenv("TESTING_CHANNEL")

# Helper functions


async def has_perms(ctx):
    has_perms = ctx.author.permissions_in(ctx.channel).manage_channels
    if not has_perms:
        await ctx.send("You do not have permission to use this command.")
    return has_perms


async def add_reaction(ctx): await ctx.message.add_reaction("✅")


async def texts_to_discord_channels(channel_ids):
    channels = []

    if testing:
        channels = [bot.get_channel(int(channel_id))
                    for channel_id in channels]
        return channels

    for channel_id in channel_ids:
        got_channel = bot.get_channel(int(channel_id))
        if got_channel is not None:
            channels.append(got_channel)
    return channels


async def request_posts(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            posts_req = await resp.json()
            return posts_req

# formatter function that sends the correct social media post


async def formatter(user, prev_time, social_media, channels, settings):
    # get all the avaliable channels
    all_channels = channels

    platform = social_media.capitalize()

    url = f"{SERVER_API}/{social_media}?username={user}&prev_time={prev_time}"
    posts_req = await request_posts(url)
    if posts_req.get("success") is False:
        return {"channels_exist": True, "api_success": False, "api_type": posts_req.get("API"), "data": posts_req.get('data'), "time_elapsed": posts_req.get("Time elapsed")}

    posts = posts_req.get("data")
    if posts == [] or posts is None:
        return {"channels_exist": True, "api_success": True, "api_type": posts_req.get("API"), "data": posts, "time_elapsed": posts_req.get("Time elapsed")}

    for p in posts:
        embed = discord.Embed(
            description=p["post_text"], color=SOCIALS_DATA[social_media]["color"], timestamp=datetime.utcfromtimestamp(p["post_timestamp"]).replace(tzinfo=timezone.utc))
        embed.set_author(
            name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
        embed.set_footer(
            text=platform, icon_url=SOCIALS_DATA[social_media]["icon"])
        if p.get("post_media_URL"):
            embed.set_image(url=p["post_media_URL"])

        if testing is True:
            new_post_str = f"**New post from {user} on {platform}**\n{p['post_URL']}\n"
            video_str = f'Click to view video' if p.get(
                'post_is_video') else ''
            channel = bot.get_channel(TESTING_CHANNEL)
            await channel.send(content=f"{new_post_str}{video_str}", embed=embed)
            return {"channels_exist": True, "API Success": True, "api_type": posts_req.get("API"), "data": posts, "time_elapsed": posts_req.get("Time elapsed")}

        for channel in all_channels:
            if channel is None:
                continue
            new_post_str = f"**New post from {user} on {platform}**\n{p['post_URL']}\n"
            video_str = f'Click to view video' if p.get(
                'post_is_video') else ''
            if settings.get("language") == "Spanish":
                new_post_str = f"**Nuevo contenido de {user} en {platform}**\n{p['post_URL']}\n"
                video_str = f'Haga clic para ver el vídeo' if p.get(
                    'post_is_video') else ''
            if settings.get("send_video_as_link") == "Yes" and p.get('post_is_video'):
                video_str = ""
                await channel.send(content=f"{new_post_str}{video_str}")
                continue
            await channel.send(content=f"{new_post_str}{video_str}", embed=embed)
    return {"channels_exist": True, "API Success": True, "api_type": posts_req.get("API"), "data": posts, "time_elapsed": posts_req.get("Time elapsed")}


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
    channels_from_db = []
    for channel_id in channels_database.get(ctx.guild.id):
        channel_resp = bot.get_channel(int(channel_id))
        if channel_resp:
            channels_from_db.append(f"#{channel_resp.name} ID:{channel_id}")

    embed = discord.Embed(title="Channels", description='\n'.join(
        channels_from_db), color=1146986)
    await ctx.send(embed=embed)
    await add_reaction(ctx)


@ listChannel.error
async def listChannel_error(ctx, error):
    if isinstance(error, commands.ArgumentParsingError):
        await ctx.send("Incorrect usage of command: `s!setChannel #{text-channel}`")


# Social Media Usernames:
@ bot.command()
async def add(ctx, social_media, user: str):
    social_media = social_media.lower()
    if not await has_perms(ctx):
        return

    # checking the first argument (platform management)
    if social_media not in SOCIALS_DATA.keys():
        await ctx.send(f"Invalid social media site entered. Available social media platforms are {', '.join(SOCIALS_DATA.keys())}.")
        return

    platform_capitalize = social_media.capitalize()
    # checks if user account doesn't exist
    url = f"{SERVER_API}/{social_media}-user?username={user}"

    resp = await request_posts(url)

    if not resp.get("data"):
        await ctx.send(f"`User {user}` does not exist on {platform_capitalize}.")
        return

    social_database.add(ctx.guild.id, social_media, user)

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
async def remove(ctx, social_media: str, user: str):
    if not await has_perms(ctx):
        return

    # checking the first argument (platform management)
    if social_media not in SOCIALS_DATA.keys():
        await ctx.send(f"Invalid social media site entered. Available social media platforms are {', '.join(SOCIALS_DATA.keys())}.")
        return

    social_database.remove(ctx.guild.id, social_media, user)

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


@ tasks.loop(minutes=28)  # repeat every 10 minutes
async def main_loop():
    failed = []
    start = time.perf_counter()
    await bot.wait_until_ready()
    for server_ids in social_database.all:
        for server_id in server_ids.keys():
            channels = channels_database.get(server_id)
            all_channels = await texts_to_discord_channels(channels)
            if not all_channels and testing == False:
                continue
            prev_time = time_database.get(server_id)
            socials = social_database.get(server_id)
            settings = settings_database.get(server_id)
            for social_media in SOCIALS_DATA.keys():
                if socials.get(social_media) is None:
                    continue
                for user in socials[social_media]:
                    params = [user, prev_time,
                              social_media, all_channels, settings, server_id]
                    print(
                        f"Server: {server_id} Channels: {channels} Settings: {settings}\nUsername: {user} on {social_media}")
                    try:
                        result = await formatter(params[0], params[1], params[2], params[3], params[4])
                        if result.get("api_success") is False:
                            print("API FAILED!!!\n" + str(result) + "\n")
                            failed.append(params)
                            continue
                    except Exception as e:
                        result = {"channels_exist": False, "api_success": False,
                                  "api_type": "ERROR", "data": repr(e), "time_elapsed": "ERROR"}
                    print("Result: " + str(result) + "\n")
            time_database.add(server_id, int(time.time()))
    finish = time.perf_counter()
    failed_meta = f"\n\n\nThis loop took: {round(finish - start, 2)} seconds which is around {round(finish - start, 2)//60} minutes\n\n\n"
    failed_info = failed_meta + str(failed)
    print(failed_info)
    with open("failed.txt", "w") as output:
        output.write(failed_info)

if __name__ == '__main__':
    main_loop.start()
    bot.run(os.getenv('DISCORD_TOKEN'))
