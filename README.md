# Announcements

Instagram is currently still not working. There will be a massive update tomorrow night that will resolve this issue hopefully permenantly.

# FTWBot

<!-- <img src="https://user-images.githubusercontent.com/89803837/160317016-a68164d4-a6fa-4fc4-8957-db3093f65c73.png" alt="Basket with social medias inside" width=300rem height=300rem> -->
<img src="https://github.com/ericf1/ftwbot/blob/main/pictures/ftw%20logo.png" width=300rem height=300rem>

A Discord bot that continuously updates and posts Instagram and Twitter posts from designated accounts. 

We are currently supporting over 196 servers!

Visit our [Top.gg](https://top.gg/bot/952690377104719964) page!

Add FTWBot To Your Server!
---
Click on the link and authenticate:
[Link](https://discord.com/api/oauth2/authorize?client_id=952690377104719964&permissions=517543905344&scope=bot)

If the first link is full:
[Second Link](https://discord.com/api/oauth2/authorize?client_id=978880834440429578&permissions=277025474624&scope=bot)

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

Requirements!
---

- **For posts to send you must have a channel set first with s!setChannel**

- **You also must ensure that the bot has permission to write in that channel or it will not be able to post!**

Future
---
- Implementing Reddit and YouTube APIs
- Creating custom web links for Discord webhooks
- Implementing Redis Database


Suggestions are appreciated and can be posted to the [Discussions](https://github.com/ericf1/ftwbot/discussions) page.

How To Set Up Your Own Bot From Your Personal Machine
---
>First, fetch our code base through git clone:
```
git clone https://github.com/ericf1/ftwbot.git
```
or through downloading the source code that is avaliable in the [versions](https://github.com/ericf1/ftwbot/releases)

>Install the necessary libraries by running:
```
pip3 install -r requirements.txt
```

>Change directories to the python code files with:
```
cd src
```

>Create a .env file containing the following inside of the src folder with vim or your favorite text editor:
```
vim .env
```

>You will need a personal Discord Token, Twitter API Key, and Twitter Access Token. Your .env file should be formatted like this:
```
TWITTER_API_KEY=
TWITTER_API_SECRET_KEY=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
DISCORD_TOKEN=
```
You can find these keys from the [Twitter Developer Portal](https://developer.twitter.com/en/portal/petition/essential/basic-info) and [Discord Developer Portal](https://discord.com/developers/docs/intro)

>In vim, to save and exit, execute:
```
:wq
```

>Start the bot with:
```
python3 bot.py
```

Our Python code is currently set to check for new posts every ten minutes (this can be changed in under the parameter of the mainLoop).

In order to constantly maintain the bot, we recommend running the Python script through a Cloud Hosting Service such as [Amazon Web Service](https://aws.amazon.com/). We currently run an instance of ubuntu through AWS. 

Questions and Inquiries
---
[ericfang1935@gmail.com](mailto:ericfang1935@gmail.com)

Technologies Used
---
Python, Discord.py, Tweepy API, TinyDB, Redis, Google API, Reddit API, Amazon Web Server

Made For
---
[The Dive Studios's Timmy Bot](https://www.divestudios.io/)

Developers
---
Eric Fang, Wilson Wuchen, Edison Tran, Trinnity Ye (Marketing), Ella Tang (Marketing)
