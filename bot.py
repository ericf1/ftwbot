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
instagram = ["edisonfang123", "mindset_dive"]
twitter = ["EricisonF", "mindset_dive", "briannam10"]
maxAccounts = len(instagram) + len(twitter)

# Setup database
db = TinyDB('database.json')
if not db.get(doc_id=1):
    db.insert({"twitter": [], "instagram": []})

# discord client commands
client = commands.Bot(command_prefix='.')

# Input the Discord Information
serverName = "egg simps ᕕ( ᐛ )ᕗ"
channelID = 452286672441442355


@client.event
async def on_ready():
    # printing out message so it looks cool
    print(f'{client.user.name} has connected to Discord!')


@ tasks.loop(minutes=1)  # repeat every minute
async def myLoop():
    await client.wait_until_ready()

    channel = client.get_channel(channelID)
    await channel.send("1 min passed: attempting to fetch:")

    doc = db.get(doc_id=1)
    prevTime = doc.get("prevTime")

    if prevTime:
        for user in doc["instagram"]:
            for p in getLatestIGPosts(user, prevTime):
                embed = discord.Embed(
                    description=p["post_text"], color=13453419)
                embed.set_author(
                    name=user, url=p["profile_URL"], icon_url=p["profile_pic_URL"])
                embed.set_image(url=p["post_picture_URL"])
                embed.add_field(name="Likes", value=f"{p['post_likes']}")
                embed.set_footer(
                    text="Instagram", icon_url="https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png")

                await channel.send(content=f"**New Post from {user}!**\n\n{p['post_URL']}", embed=embed)

    db.update({"prevTime": time.time()}, doc_ids=[1])


# .ping will respond pong to ensure that the bot is alive
@ client.command()
async def ping(ctx):
    await ctx.send('Pong')


@ client.command()
async def test(ctx):
    embed = discord.Embed(
        description="too cool!",
        url="https://www.instagram.com/p/CbVpJMappfe/",
        color=13453419,
    )
    embed.set_author(name="edisonfang123",
                     url="https://www.instagram.com/edisonfang123",
                     icon_url="https://instagram.fjdh1-1.fna.fbcdn.net/v/t51.2885-19/44884218_345707102882519_2446069589734326272_n.jpg?efg=eyJybWQiOiJpZ19hbmRyb2lkX21vYmlsZV9uZXR3b3JrX3N0YWNrX3F1aWNfa2VlcF9hbGl2ZV81X3RvXzIwczoyMHMifQ&_nc_ht=instagram.fjdh1-1.fna.fbcdn.net&_nc_cat=1&_nc_ohc=XvygljXaX5wAX-vcmS_&edm=ABmJApABAAAA&ccb=7-4&ig_cache_key=YW5vbnltb3VzX3Byb2ZpbGVfcGlj.2-ccb7-4&oh=00_AT_c_9FanzZDT4WuFzgq6-0G2oTOfD7ZTyIiOwiACb4zNA&oe=623E770F&_nc_sid=6136e7")
    embed.set_image(url="https://scontent-lga3-1.cdninstagram.com/v/t51.2885-15/276003015_1014255279526381_4404476007183939739_n.jpg?stp=dst-jpg_e35_s640x640_sh0.08&_nc_ht=scontent-lga3-1.cdninstagram.com&_nc_cat=101&_nc_ohc=KCTH6RFYPVUAX_U8xKA&edm=AAuNW_gBAAAA&ccb=7-4&oh=00_AT8BJD3x9OkZsExZHLLxzs8c7R7QQw5yP62Juujl3ry1Cw&oe=623E04EF&_nc_sid=498da5")
    embed.add_field(name="Likes", value="1",)
    embed.set_footer(
        text="Instagram",
        icon_url="https://www.instagram.com/static/images/ico/favicon-192.png/68d99ba29cc8.png")
    # embed.timestamp = date.today()

    await ctx.send(content="**New Post from edisonfang123!**\n\nhttps://www.instagram.com/p/CbVpJMappfe/", embed=embed)


# Wilson's logging thing
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

myLoop.start()
client.run(os.getenv('DISCORD_TOKEN'))
