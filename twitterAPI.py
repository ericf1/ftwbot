#Load the dotenv library and then the dotenv file
from dotenv import load_dotenv 
load_dotenv()

import os
import tweepy

TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_KEY = os.getenv('TWITTER_ACCESS_KEY')
TWITTER_ACCESS_SECRET_TOKEN = os.getenv('TWITTER_ACCESS_SECRET_TOKEN')

#Authentication object
authenticate = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)

#Access token and Access Token secret
authenticate.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET_TOKEN)

#API object to pass in auth info
api = tweepy.API(authenticate, wait_on_rate_limit = True)

#Function that returns the latest tweet from a given screenname
def latestTweet(username):
    postId = api.user_timeline(screen_name=f"{username}", count=1)[0].id
    return f"https://twitter.com/{username}/status/{postId}"

print(latestTweet('elonmusk'))