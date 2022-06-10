from sync_instagramapi import get_latest_instagram_post, check_instagram_user
from sync_twitterapi import get_latest_twitter_post, check_twitter_user
from flask import Flask, jsonify, request
import json
import asyncio

app = Flask(__name__)


@app.route('/')
def hello():
    return 'hello'


@app.route('/instagram')
def instagram():
    username = request.args.get('username')
    prev_time = str(request.args.get('prev_time'))
    response = {"data": get_latest_instagram_post(
        username, prev_time), "success": True}
    print(get_latest_instagram_post(
        username, prev_time))
    return response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
