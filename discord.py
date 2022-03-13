from twitterAPI import latestTweet
from instagramAPI import latestIGPost

import time

# input instagram username and twitter username
usernameIG = "edisonfang123"
usernameTwitter = ""

oldTweetLink = ""
oldIGLink = ""


def embeddedLink(link):
    print(link['link'])


# Loop to run continously check
while(True):
    if(usernameTwitter):
        latestTweetLink = latestTweet(usernameTwitter)
        if(oldTweetLink != latestTweetLink["link"]):
            embeddedLink(latestTweetLink)
            oldTweetLink = latestTweetLink["link"]

    if(usernameIG):
        latestIGLink = latestIGPost(usernameIG)
        if(oldIGLink != latestIGLink["link"]):
            embeddedLink(latestIGLink)
            oldIGLink = latestIGLink["link"]
    time.sleep(15)
