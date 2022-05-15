# Load the dotenv library and then the dotenv file
import tweepy
import os
import time
from dotenv import load_dotenv
load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET_KEY'), os.getenv(
    'TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

# API object to pass in auth info
api = tweepy.API(auth, wait_on_rate_limit=True)


def getLatestTwitterPosts(username, prevFetchTime):
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
            while i < len(tweetsData) and tweetsData[i].created_at.timestamp() > prevFetchTime:
                tweetData = tweetsData[i]._json

                data = dict()
                data["post_id"] = tweetData["id"]
                data["post_URL"] = f"https://twitter.com/{username}/status/{data['post_id']}"
                data["post_timestamp"] = tweetsData[i].created_at.timestamp()

                if tweetData.get("extended_entities") and tweetData["extended_entities"].get("media")[0]:
                    mediaData = tweetData["extended_entities"]["media"][0]

                    data["post_isVideo"] = True if mediaData["type"] == "video" else False
                    data["post_media_URL"] = mediaData["media_url"]

                data["post_text"] = tweetData["full_text"]

                allData.append({**profileData, **data})
                i += 1
    except Exception as e:
        print(repr(e))
        allData = None
    return allData


def checkTwitterUser(username):
    try:
        api.get_user(screen_name=username)
        return True
    except:
        return False


if __name__ == '__main__':
    username = ''

    start = time.perf_counter()
    getLatestTwitterPosts(username, 1)
    finish = time.perf_counter()
    print(f'finished in {round(finish-start, 2)} seconds(s)')
