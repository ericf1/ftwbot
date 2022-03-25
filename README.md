# FTWBot

A custom discord bot that continuously updates and posts Instagram and Twitter news from designated accounts.

## General Use

[Link To Authenticate Bot Into Server](https://discord.com/api/oauth2/authorize?client_id=952690377104719964&permissions=517543905344&scope=bot)

## Setup Information

You need a personal Discord Token, Twitter API Key, and Twitter Access Token

> Create a .env file containing the following variables

```
TWITTER_API_KEY=?
TWITTER_API_SECRET_KEY=?
TWITTER_ACCESS_TOKEN=?
TWITTER_ACCESS_TOKEN_SECRET=?
DISCORD_TOKEN=?
```

> You can find these keys from the [Twitter Developer Portal](https://developer.twitter.com/en/portal/petition/essential/basic-info) and [Discord Developer Portal](https://discord.com/developers/docs/intro)

To choose an account to track, edit the 'bot.py' file and change the account names to whichever one you would like to follow.

In order to constantly maintain the bot, we recommend running the Python script (python3 bot.py) through a Cloud Hosting Service such as [Amazon Web Service](https://aws.amazon.com/). The program is set to check for new posts every minute.

To install the different libraries run:

```
pip3 install -r requirements.txt
```
