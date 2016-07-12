#!/usr/bin/env python3
# Bot that tweets about Firehouse films

from composer import tweet_this, composetweet
import tweepy
from creds import consumer_key, consumer_secret, access_token, access_token_secret
from time import sleep

def tweet():
    text = composetweet(tweet_this())
    api.update_status(status = text)
    print(text)

if __name__ == "__main__":
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        tweet()
    except tweepy.error.TweepError as e:
        print(e)
        sleep(15 * 60)
        tweet()
    except Exception as e:
        print(e)
        raise

