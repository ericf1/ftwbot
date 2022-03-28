# FTWBot

<img src="https://user-images.githubusercontent.com/89803837/160317016-a68164d4-a6fa-4fc4-8957-db3093f65c73.png" width=300rem height=300rem>

A custom discord bot that continuously updates and posts Instagram and Twitter news from designated accounts.

General Use
---
[Link To Authenticate Bot Into Server](https://discord.com/api/oauth2/authorize?client_id=952690377104719964&permissions=517543905344&scope=bot)

Features
---
- Easy to run (See Setup Information below)
- Constant uptime (See Setup Information below)
- Supports both Instagram and Twitter

Commands
---
FTWBot's prefix is ``s!``, add it to the start of any of this bot's command. All of the commands are case-sensitive.

| Command | Arguments | Description | Example |
|---------|-----------|-------------|---------|
| setChannel | ``{#channel}`` | Sets the channel the bot posts in | ``s!setChannel #general``|
| list | None | Displays a list of all of the social media accounts being tracked | ``s!list``|
| add |``{social-media-platform} {username}`` | Adds a social media account to the list of accounts being tracked | ``s!add twitter lsxyz9`` | 
| delete | ``{social-media-platform} {username}`` | Removes a social media account from the list of accounts being tracked | ``s!delete twitter Cloud9``|
| ping | None | Pong | ``s!ping`` |


Future
---
- Implementing other platforms
- Creating custom web links for Discord webhooks


Suggestions are appreciated and can be posted to the [Discussions](https://github.com/ericf1/ftwbot/discussions) page.

How To Set Up Your Own Bot
---
You need a personal Discord Token, Twitter API Key, and Twitter Access Token
>Create a .env file containing the following (replace the question marks):
```
TWITTER_API_KEY=
TWITTER_API_SECRET_KEY=
TWITTER_ACCESS_TOKEN=
TWITTER_ACCESS_TOKEN_SECRET=
DISCORD_TOKEN=
```
>You can find these keys from the [Twitter Developer Portal](https://developer.twitter.com/en/portal/petition/essential/basic-info) and [Discord Developer Portal](https://discord.com/developers/docs/intro)

To choose an account to track, edit the 'bot.py' file and change the account names to whichever one you would like to follow.

In order to constantly maintain the bot, we recommend running the Python script (python3 bot.py) through a Cloud Hosting Service such as [Amazon Web Service](https://aws.amazon.com/). The program is set to check for new posts every minute.

To install the different libraries run:
```
pip3 install -r requirements.txt
```

Technologies Used
---
Python, Discord Python API, Tweepy API, TinyDB, Amazon Web Server

Made By
---
Eric Fang, Wilson Wuchen, Edison Tran, Trinnity Ye (Picture)
