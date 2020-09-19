#!/usr/bin/env python3
"""Bot that tweets about Firehouse films"""

import os

import tweepy

from composer import Films

def main() -> None:
    """Entry point"""
    auth = tweepy.OAuthHandler(os.environ["CONSUMER_KEY"],
                               os.environ["CONSUMER_SECRET"])
    auth.set_access_token(os.environ["ACCESS_TOKEN"],
                          os.environ["ACCESS_TOKEN_SECRET"])
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    films = Films()
    film = films.choice()

    api.update_status(status=film.text())
    print(film.text())

if __name__ == "__main__":
    main()
