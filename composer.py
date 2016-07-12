#!/usr/bin/env python3
# Compose tweets about Firehouse films

import json
import re
from html import unescape
from bs4 import BeautifulSoup
from random import choice

alreadytweeted = []

class Film(object):
    def __init__(self, data):
        #self.data = data
        self.title = unescape(data["title"])
        self.firehouse_no = data["categories"][0]["title"].split()[0][1:]
        #self.firehouse_name = unescape(" ".join(data["categories"][0]["title"].split()[1:]))
        self.url = data["url"][7:]  # strip "http://"
        #self.img_url = data["thumbnail_images"]["large"]["url"]
        self.categories = data["categories"]
        self.excerpt = unescape(nohtml(data["excerpt"])).strip()
        self.content= data["content"]

        self.winner = []
        if len(self.categories) > 1:
            for i in range(1, len(self.categories)):
                self.winner.append(self.categories[i]["title"])

    def videourl(self):
        videourl = []
        soup = BeautifulSoup(self.content, "html.parser")
        for link in soup.findAll("a"):
            videourl.append(link.get("href"))
        for url in videourl:
            #if "https://www.youtube.com/" in url:
            if url.startswith("https://"):
                if "youtu" or "vimeo" in url:
                    return url
        return ""
    
    def humans(self):
        from handles import handlemap
        handles = []
        for key in handlemap:
            if key.lower() in self.excerpt.lower():
                handles.append(handlemap[key])
        return handles

def nohtml(text):
    return re.sub("<[^<]+?>", "", text)

def filmlist():
    #wget http://firehousefilmcontest.com/?json=1 -O ffc.json
    f = open("ffc.json", "r").read() 
    f = json.loads(f)
    films = []
    for i in range(len((f["posts"]))):
        film = Film(f["posts"][i])
        films.append(film)
    return films

def composetweet(film):
    tweet = ""
    if film.winner:
        tweet = "Winner of "
        for prize in film.winner:
            tweet += prize.lower() + ", "
        tweet = tweet[:-2] + " in "
    else:
        tweet = "From "

    tweet += "Firehouse " + film.firehouse_no + ", \"" + film.title + "\""
    
    if film.humans():
        tweet += " by "
        for human in film.humans():
            tweet += "@" + human + ", "
        tweet = tweet[:-2]
    
    tweet += ": " + film.url + ". " + film.videourl()

    return tweet

def charactercount(film):
    cc = len(composetweet(film)) - len(film.url) - len(film.videourl()) + 2 * 23
    return cc

def tweet_this():
    film = choice(filmlist())
    if charactercount(film) <= 140 and film not in alreadytweeted:
        alreadytweeted.append(film)
        if len(alreadytweeted) > 30:
            alreadytweeted[:] = alreadytweeted[1:]
        return film
    else:
        return tweet_this()

if __name__ == "__main__":
    for i in range(60):
        print(tweet_this())
        print(len(alreadytweeted))

