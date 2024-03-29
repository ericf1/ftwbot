# Announcements

Join for our support server for updates about the bot! [Invite](https://discord.gg/Wu8wYvrSx4)

As you may have noticed, the bot is currently down, and I am working as much during my free time to solve the current issue with my Instagram integration. Thank you so much for your patience.

# FTWBot

<!-- <img src="https://user-images.githubusercontent.com/89803837/160317016-a68164d4-a6fa-4fc4-8957-db3093f65c73.png" alt="Basket with social medias inside" width=200rem height=200rem> -->
<div display="flex" flex-direction="column">
  <img src="https://github.com/ericf1/ftwbot/blob/main/pictures/ftw%20logo.png" width=210rem height=210rem>
  <img src="https://github.com/ericf1/ftwbot/blob/main/pictures/ftwbot2.png" width=210rem height=210rem>
  <img src="https://github.com/ericf1/ftwbot/blob/main/pictures/ftwlogo3.png" width=210rem height=210rem>
  <img src="https://github.com/ericf1/ftwbot/blob/main/pictures/ftwbot4.png" width=210rem height=210rem>
</div>

A Discord bot that continuously updates and posts Instagram and Twitter posts from designated accounts. 

We are currently supporting over 310 servers!

Visit our [Top.gg](https://top.gg/bot/952690377104719964) page!

Add FTWBot To Your Server!
---
Click on the link and authenticate:
[Link](https://discord.com/api/oauth2/authorize?client_id=952690377104719964&permissions=517543905344&scope=bot)

If the first link is full:
[Second Link](https://discord.com/api/oauth2/authorize?client_id=978880834440429578&permissions=277025474624&scope=bot)

If the second link is full:
[Third Link](https://discord.com/api/oauth2/authorize?client_id=989295540938362890&permissions=277025474624&scope=bot)

If the third link is full:
[Fourth Link](https://discord.com/api/oauth2/authorize?client_id=995839397150863360&permissions=277025474624&scope=bot)

Features
---
- Notify your server about Instagram posts and tweets from yourself or your favorite influencers!
- Easy and intitutive set up and constant support. Just set it and forget it!
- 24/7 runtime on cloud servers!

Commands
---
FTWBot's prefix is ``s!``, add it to the start of any of this bot's command.

| Command | Arguments | Description | Example |
|---------|-----------|-------------|---------|
| addChannel | ``{#channel} or None`` | Adds a channel for the bot to post in (no arguments means that it will add the channel where you wrote the command) | ``s!addChannel``|
| listChannel | None | Displays a list of the channels with their IDs that the bot is going to post in | ``s!listChannel``|
| removeChannel | ``{#channel}`` | Removes the selected channel from the list of channels to be sent | ``s!removeChannel #general``|
| add |``{social-media-platform} {username}`` | Adds a social media account to the list of accounts being tracked | ``s!add twitter lsxyz9`` | 
| list | None | Displays a list of the social media accounts being tracked | ``s!list``|
| remove | ``{social-media-platform} {username}`` | Removes a social media account from the list of accounts being tracked | ``s!remove twitter Cloud9``|
| settings | ``None`` | Lists the avaliable settings to change | ``s!settings``|
| setSettings | ``{setting}`` or ``{setting} default`` | Follow a series of prompts to update your selected setting. Default parameter will give you back the default setting. | ``s!setSettings announcement_msg_for_post``|
| ping | None | Pong | ``s!ping`` |

Requirements!
---

- **For posts to send you must have a channel add first with s!addChannel**

- **You also must ensure that the bot has permission to write in that channel or it will not be able to post!**

Future
---
- Implementing Reddit and YouTube APIs
- Creating custom web links for Discord webhooks
- Having settings to edit how the messages are formatted
- Logging and posting your own scheduled posts


Suggestions are appreciated and can be posted to the [Discussions](https://github.com/ericf1/ftwbot/discussions) page or in our Discord Server.

How To Set Up Your Own Bot From Your Personal Machine
---
>First, download the v0.1.3 code base. This version is supported by TinyDB which can run on local machines:
[versions](https://github.com/ericf1/ftwbot/releases)

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

>To start inserting with vim, you need to write:
```
i
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

Change the main_loop function's decorator argument in order to edit the time which you request to see if there are any new posts.

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
Eric Fang
