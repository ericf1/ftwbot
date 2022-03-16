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

"""
profile url
profile picture url
timestamp
post url
picture url / video url (optional)
likes
retweets

if tweet = retweet:
    continue
"""


def getLatestTweets(username):
    profileData = dict()
    allData = []
    try:
        tweetsData = api.user_timeline(screen_name=f"{username}", count=20, tweet_mode="extended")

        data = dict()

        data["post_id"] = tweetsData[0]["id"]
        data["link"] = f"https://twitter.com/{username}/status/{postId}"
        data["timestamp"] = data.created_at
        data["text"] = tweetsData[0]["full_text"]
        data["user"] = tweetsData[0]["user"]["name"]
    except:
        data["link"] = ""
        data["timestamp"] = None
        data["text"] = None
        data["user"] = None

    return data


# testing method
# print(latestTweet('elonmusk')["link"])
# print(latestTweet('elonmusk')["timestamp"])
# print(latestTweet('elonmusk')["text"])
# print(latestTweet('elonmusk')["user"])
