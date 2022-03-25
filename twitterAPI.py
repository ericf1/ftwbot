# Load the dotenv library and then the dotenv file
import time
import datetime
from re import T
import tweepy
import os
from dotenv import load_dotenv
load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET_KEY'), os.getenv(
    'TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

# API object to pass in auth info
api = tweepy.API(auth, wait_on_rate_limit=True)


def getLatestTweets(username, prevFetchTime):
    profileData = dict()
    allData = []
    try:
        tweetsData = api.user_timeline(
            screen_name=f"{username}", count=20, tweet_mode="extended", exclude_replies=True, include_rts=False)

        if tweetsData[0]._json["user"]:
            userData = tweetsData[0]._json["user"]
            profileData["profile_name"] = userData["name"]
            profileData["profile_URL"] = f"https://twitter.com/{username}"
            profileData["profile_pic_URL"] = userData["profile_image_url_https"]

            i = 0
            while i < len(tweetsData) and time.mktime(tweetsData[i].created_at.timetuple()) > prevFetchTime:

                tweetData = tweetsData[i]._json

                data = dict()
                data["post_id"] = tweetData["id"]
                data["post_URL"] = f"https://twitter.com/{username}/status/{data['post_id']}"
                data["post_timestamp"] = tweetsData[i].created_at

                if tweetData.get("extended_entities") and tweetData["extended_entities"].get("media")[0]:
                    mediaData = tweetData["extended_entities"]["media"][0]

                    data["post_isVideo"] = True if mediaData["type"] == "video" else False
                    data["post_media_URL"] = mediaData["media_url"]

                data["post_text"] = tweetData["full_text"]

                # data["post_text"] = tweetData["full_text"]
                # data["post_likes"] = tweetData["favorite_count"]
                # data["post_retweets"] = tweetData["retweet_count"]

                # print(i)
                # print(data["post_URL"], data["post_timestamp"])

                allData.append({**profileData, **data})
                i += 1
    except Exception as e:
        print(repr(e))
        allData = None
    return allData


# getLatestTweets("EricisonF", 1647316800)
# getLatestTweets("elonmusk", 1647662400)
