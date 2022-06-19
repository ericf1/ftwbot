import tweepy
import os
from dotenv import load_dotenv
import time

load_dotenv()

auth = tweepy.OAuthHandler(os.getenv('TWITTER_API_KEY'), os.getenv('TWITTER_API_SECRET_KEY'), os.getenv(
    'TWITTER_ACCESS_TOKEN'), os.getenv('TWITTER_ACCESS_TOKEN_SECRET'))

api = tweepy.API(auth, wait_on_rate_limit=True)


def api_request(username):
    return api.user_timeline(
        screen_name=f"{username}", count=10, tweet_mode="extended", exclude_replies=True, include_rts=False)


def get_latest_twitter_post(username, prev_fetch_time):
    profile_data = dict()
    all_data = []
    try:
        tweets_data = api_request(username)

        if tweets_data[0]._json["user"]:
            user_data = tweets_data[0]._json["user"]
            profile_data["profile_name"] = user_data["name"]
            profile_data["profile_URL"] = f"https://twitter.com/{username}"
            profile_data["profile_pic_URL"] = user_data["profile_image_url_https"]

            for tweet_data in tweets_data:
                tweet_timestamp = tweet_data.created_at.timestamp()
                if tweet_timestamp > prev_fetch_time:
                    tweet_data = tweet_data._json

                    data = dict()
                    data["post_id"] = tweet_data["id"]
                    data["post_URL"] = f"https://twitter.com/{username}/status/{data['post_id']}"
                    data["post_timestamp"] = tweet_timestamp

                    if tweet_data.get("extended_entities") and tweet_data["extended_entities"].get("media")[0]:
                        mediaData = tweet_data["extended_entities"]["media"][0]

                        data["post_isVideo"] = True if mediaData["type"] == "video" else False
                        data["post_media_URL"] = mediaData["media_url"]

                    data["post_text"] = tweet_data["full_text"]

                    all_data.append({**profile_data, **data})
    except Exception as e:
        print(repr(e))
        all_data = []
    return all_data


def check_twitter_user(username):
    try:
        api.get_user(screen_name=username)
        return True
    except:
        return False


def main():
    start = time.perf_counter()
    posts = get_latest_twitter_post('elonmusk', 1)
    print(posts)
    finish = time.perf_counter()

    print(f'finished in {round(finish-start, 2)} seconds(s)')


if __name__ == "__main__":
    main()
