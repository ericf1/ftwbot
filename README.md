# FTWBot

<img src="https://user-images.githubusercontent.com/89803837/160317016-a68164d4-a6fa-4fc4-8957-db3093f65c73.png" alt="Basket with social medias inside" width=300rem height=300rem>

A Discord bot that continuously updates and posts Instagram and Twitter posts from designated accounts. 

We are currently supporting over 100 servers and are in the process of getting verified as a Discord bot!

Visit our [Top.gg](https://top.gg/bot/952690377104719964) page!

Add FTWBot To Your Server!
---
Click on the link and authenticate:
[Link](https://discord.com/api/oauth2/authorize?client_id=952690377104719964&permissions=517543905344&scope=bot)

Features
---
- Easy to run
- Constant uptime
- Supports both Instagram and Twitter

Commands
---
FTWBot's prefix is ``s!``, add it to the start of any of this bot's command. All of the commands are case-sensitive.

| Command | Arguments | Description | Example |
|---------|-----------|-------------|---------|
| setChannel | ``{#channel}`` | Sets the channel the bot posts in | ``s!setChannel #general``|
| list | None | Displays a list of all of the social media accounts being tracked | ``s!list``|
| add |``{social-media-platform} {username}`` | Adds a social media account to the list of accounts being tracked | ``s!add twitter lsxyz9`` | 
| remove | ``{social-media-platform} {username}`` | Removes a social media account from the list of accounts being tracked | ``s!remove twitter Cloud9``|
| ping | None | Pong | ``s!ping`` |

*Note that for posts to send you must have a channel set first with s!setChannel!

Future
---
- Implementing Reddit and YouTube APIs
- Creating custom web links for Discord webhooks
- Implemmenting Redis Database


Suggestions are appreciated and can be posted to the [Discussions](https://github.com/ericf1/ftwbot/discussions) page.

How To Set Up Your Own Bot From Your Personal Machine
---
>First, fetch our code base through git clone:
```
git clone https://github.com/ericf1/ftwbot.git
```
or through downloading the source code that is avaliable in the [versions](https://github.com/ericf1/ftwbot/releases)

>Create a .env file containing the following inside of the src folder:
You will need a personal Discord Token, Twitter API Key, and Twitter Access Token
```
TWITTER_API_KEY=
TWITTER_API_SECRET_KEY=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
DISCORD_TOKEN=
```
You can find these keys from the [Twitter Developer Portal](https://developer.twitter.com/en/portal/petition/essential/basic-info) and [Discord Developer Portal](https://discord.com/developers/docs/intro)

>Install the necessary libraries by running:
```
pip3 install -r requirements.txt
```

>Start the bot with:
```
python3 bot.py
```

Our Python code is currently set to check for new posts every two minutes (this can be changed in under the parameter of the mainLoop).

In order to constantly maintain the bot, we recommend running the Python script through a Cloud Hosting Service such as [Amazon Web Service](https://aws.amazon.com/). We currently run an instance of ubuntu through AWS. 

Technologies Used
---
Python, Discord Python API, Tweepy API, TinyDB, Amazon Web Server

Made For
---
[The Dive Studios's Timmy Bot](https://www.divestudios.io/)

Developers
---
Eric Fang, Wilson Wuchen, Edison Tran, Trinnity Ye (Marketing), Ella Tang (Marketing)
