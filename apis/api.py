from redditapi import check_subreddit, get_latest_subreddit_posts
from instagramapi import InstagramAPI
from twitterapi import get_latest_twitter_post, check_twitter_user
from youtubeapi import get_latest_youtube_post, check_youtube_user
from flask import Flask, jsonify, request
import asyncio
import time
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
instagram_api = InstagramAPI()


def restart_cookies():
    instagram_api = InstagramAPI()
    print("Cookies have been reset!")


scheduler = BackgroundScheduler()
scheduler.add_job(func=restart_cookies, trigger="interval", minutes=45)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def asyncify(function, *args):
    asyncio.set_event_loop(asyncio.new_event_loop())
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(function(*args))
    return result


@app.route('/')
def hello():
    return 'hello'


@app.route('/instagram', methods=["GET"])
def instagram():
    start = time.perf_counter()
    username = request.args.get('username')
    prev_time = int(request.args.get('prev_time'))
    result = asyncify(instagram_api.get_latest_instagram_post,
                      username, prev_time)
    finish = time.perf_counter()
    result.update({"Time elapsed": f"{round(finish-start, 2)} seconds(s)"})
    if not result.get("success"):
        return jsonify(result), 500
    return jsonify(result), 202


@app.route('/twitter', methods=["GET"])
def twitter():
    start = time.perf_counter()
    username = request.args.get('username')
    prev_time = int(request.args.get('prev_time'))
    result = asyncify(get_latest_twitter_post, username, prev_time)
    finish = time.perf_counter()
    result.update({"Time elapsed": f"{round(finish-start, 2)} seconds(s)"})
    if not result.get("success"):
        return jsonify(result), 500
    return jsonify(result), 202


@app.route('/youtube', methods=["GET"])
def youtube():
    start = time.perf_counter()
    username = request.args.get('username')
    prev_time = int(request.args.get('prev_time'))
    result = asyncify(get_latest_youtube_post, username, prev_time)
    finish = time.perf_counter()
    result.update({"Time elapsed": f"{round(finish-start, 2)} seconds(s)"})
    if not result.get("success"):
        return jsonify(result), 500
    return jsonify(result), 202


@app.route('/reddit', methods=["GET"])
def reddit():
    start = time.perf_counter()
    username = request.args.get('username')
    prev_time = int(request.args.get('prev_time'))
    result = asyncify(get_latest_subreddit_posts, username, prev_time)
    finish = time.perf_counter()
    result.update({"Time elapsed": f"{round(finish-start, 2)} seconds(s)"})
    if not result.get("success"):
        return jsonify(result), 500
    return jsonify(result), 202


@app.route('/twitter-user', methods=["GET"])
def twitter_user():
    start = time.perf_counter()
    username = request.args.get('username')
    result = asyncify(check_twitter_user, username)
    finish = time.perf_counter()
    result.update({"Time elapsed": f"{round(finish-start, 2)} seconds(s)"})
    if not result.get("success"):
        return jsonify(result), 500
    return jsonify(result), 202


@app.route('/instagram-user', methods=["GET"])
def instagram_user():
    start = time.perf_counter()
    username = request.args.get('username')
    result = asyncify(instagram_api.check_instagram_user, username)
    finish = time.perf_counter()
    result.update({"Time elapsed": f"{round(finish-start, 2)} seconds(s)"})
    if not result.get("success"):
        return jsonify(result), 500
    return jsonify(result), 202


@app.route('/youtube-user', methods=["GET"])
def youtube_user():
    start = time.perf_counter()
    username = request.args.get('username')
    result = asyncify(check_youtube_user, username)
    finish = time.perf_counter()
    result.update({"Time elapsed": f"{round(finish-start, 2)} seconds(s)"})
    if not result.get("success"):
        return jsonify(result), 500
    return jsonify(result), 202


@app.route('/reddit-user', methods=["GET"])
def subreddit():
    start = time.perf_counter()
    username = request.args.get('username')
    result = asyncify(check_subreddit, username)
    finish = time.perf_counter()
    result.update({"Time elapsed": f"{round(finish-start, 2)} seconds(s)"})
    if not result.get("success"):
        return jsonify(result), 500
    return jsonify(result), 202


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
