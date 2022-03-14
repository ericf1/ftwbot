# Load the dotenv library and then the dotenv file
import tweepy
import os
from dotenv import load_dotenv
load_dotenv()


TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_KEY = os.getenv('TWITTER_ACCESS_KEY')
TWITTER_ACCESS_SECRET_TOKEN = os.getenv('TWITTER_ACCESS_SECRET_TOKEN')

# Authentication object
authenticate = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)

# Access token and Access Token secret
authenticate.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET_TOKEN)

# API object to pass in auth info
api = tweepy.API(authenticate, wait_on_rate_limit=True)

# Function that returns the latest tweet from a given screenname


def latestTweet(username):
    latestTweetData = dict()
    try:
        data = api.user_timeline(
            screen_name=f"{username}", count=1, tweet_mode="extended")[0]
        postId = data.id
        latestTweetData["link"] = f"https://twitter.com/{username}/status/{postId}"
        latestTweetData["timestamp"] = data.created_at
        latestTweetData["text"] = data.full_text
        latestTweetData["user"] = data.user.name
    except:
        latestTweetData["link"] = ""
        latestTweetData["timestamp"] = None
        latestTweetData["text"] = None
        latestTweetData["user"] = None

    return latestTweetData


# testing method
# print(latestTweet('elonmusk')["link"])
# print(latestTweet('elonmusk')["timestamp"])
# print(latestTweet('elonmusk')["text"])
# print(latestTweet('elonmusk')["user"])
