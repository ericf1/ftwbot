# ftwbot
A custom discord bot that continuously updates and posts Instagram and Twitter news from designated accounts.

YOU NEED YOUR OWN PERSONAL TWITTER API KEY, ACCESS TOKEN, AND DISCORD TOKEN.
Create a .env file containing the following (replace the question marks):

TWITTER_API_KEY=??????
TWITTER_API_SECRET_KEY=????????
TWITTER_ACCESS_TOKEN=??????
TWITTER_ACCESS_TOKEN_SECRET=?????????
DISCORD_TOKEN=???????

You can find these keys from the [Twitter Developer Portal](https://developer.twitter.com/en/portal/petition/essential/basic-info) and [Discord Developer Portal](https://discord.com/developers/docs/intro)

To choose an account to track, edit the 'bot.py' file and change the account names to whichever one you would like to follow.

In order to constantly maintain the bot, we recommend using a Cloud Hosting Service such as [Amazon Web Service](https://aws.amazon.com/).
We followed this [guide](https://towardsaws.com/building-hosting-a-discord-bot-on-aws-e157bd7faf78) in order to run our bot.
