#!/usr/bin/env python3
"""Bot that tweets about Firehouse films"""

import os
import time

import tweepy

from composer import Films

def tweet(api: tweepy.API, films: Films) -> None:
    """Send a tweet"""
    film = films.get_film()
    api.update_status(status=film.tweet.text)
    print(film.tweet)

def main() -> None:
    """Entry point"""
    auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"],
                               os.environ["CONSUMER_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"],
                          os.environ["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    films = Films()

    try:
        tweet(api, films)
    except tweepy.error.TweepError as exception:
        print(exception)
        time.sleep(15 * 60)
        tweet(api, films)

if __name__ == "__main__":
    main()
