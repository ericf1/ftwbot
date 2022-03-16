# Load the dotenv library and then the dotenv file
from re import T
import tweepy
import os
from dotenv import load_dotenv
load_dotenv()


TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
TWITTER_API_SECRET_KEY = os.getenv('TWITTER_API_SECRET_KEY')
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN')
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')

auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY,
                           TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET)

# API object to pass in auth info
api = tweepy.API(auth, wait_on_rate_limit=True)

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
    media = []
    try:
        tweetsData = api.user_timeline(
            user_id=f"{username}", count=20, tweet_mode="extended", exclude_replies=True, include_rts=False)

        if tweetsData[0]._json["user"]:
            userData = tweetsData[0]._json["user"]
            profileData["profile_name"] = userData["name"]
            profileData["profile_URL"] = f"https://twitter.com/{username}"
            profileData["profile_pic_URL"] = userData["profile_image_url_https"]

            i = 0
            while i < len(tweetsData) and tweetsData[i].created_at:

                tweetData = tweetsData[i]._json

                data = dict()
                data["post_id"] = tweetData["id"]
                data["post_URL"] = f"https://twitter.com/{username}/status/{data['post_id']}"
                data["post_timestamp"] = tweetsData[i].created_at

                if tweetData.get("extended_entities") and tweetData["extended_entities"].get("media")[0]:
                    mediaData = tweetData["extended_entities"]["media"][0]
                    media.append(mediaData)

                    data["post_isVideo"] = True if mediaData.type == "video" else False
                    if data["post_isVideo"]:
                        data["post_video_frame_URL"] = mediaData["media_url_https"]
                        # data["post_video_URL"] = mediaData["video_url"]
                    # else:
                        # data["post_picture_URL"] = mediaData["display_url"]

                    print(i)
                    print(mediaData)
                    zzzzzzzz = 1

                data["post_text"] = tweetData["full_text"]
                data["post_likes"] = tweetData["favorite_count"]
                data["post_retweets"] = tweetData["retweet_count"]

                # print(data["post_URL"])
                i += 1
    except Exception as e:
        print(repr(e))
        data = None
    # return data


# testing method
# print(latestTweet('elonmusk')["link"])
# print(latestTweet('elonmusk')["timestamp"])
# print(latestTweet('elonmusk')["text"])
# print(latestTweet('elonmusk')["user"])

getLatestTweets("EricisonF")
