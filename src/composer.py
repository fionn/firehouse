#!/usr/bin/env python3
"""Compose tweets about Firehouse films"""

import re
import json
import html
import random
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup

# pylint: disable=too-few-public-methods
class FilmTweet:
    """Just the text, pretty much"""

    def __init__(self, film: "Film") -> None:
        self.film = film
        self.text = self._compose_tweet()

    def _compose_tweet(self) -> str:
        """Compose a tweet about a film"""
        tweet = ""
        if self.film.awards:
            tweet = "Winner of " + ", ".join(self.film.awards) + " in "
        else:
            tweet = "From "
        tweet += f"Firehouse {self.film.firehouse_no}, “{self.film.title}”"
        if self.film.humans:
            tweet += " by " + ", ".join(["@" + human for human in self.film.humans])
        tweet += f": {self.film.url}. {self.film.video_url}"
        return tweet

    def __len__(self) -> int:
        return len(self.text) - len(self.film.url) - len(self.film.video_url) + 2 * 23

    def __repr__(self) -> str:
        return self.text

    def __str__(self) -> str:
        return self.__repr__()

class Film:
    """Film metadata"""

    def __init__(self, data: dict) -> None:
        self.title = html.unescape(data["title"])
        self.categories = data["categories"]
        self.firehouse_no = self.categories[0]["title"].split()[0][1:]
        self.url = data["url"].split("http://", maxsplit=1)[1]
        self.excerpt = html.unescape(no_html(data["excerpt"])).strip()
        self.content = data["content"]
        self.tweet = FilmTweet(self)
        #self.firehouse_name = unescape(" ".join(data["categories"][0]["title"].split()[1:]))
        #self.img_url = data["thumbnail_images"]["large"]["url"]

    @property
    def awards(self) -> List[str]:
        """List of awards the film won"""
        winner: List[str] = []
        if len(self.categories) > 1:
            for i in range(1, len(self.categories)):
                winner.append(self.categories[i]["title"].lower())
        return winner

    @property
    def video_url(self) -> str:
        """URL to film host"""
        soup = BeautifulSoup(self.content, "html.parser")
        for link in soup.findAll("a"):
            url = link.get("href")
            if url.startswith("https://"):
                if "youtu" or "vimeo" in url:
                    return url.split("&", maxsplit=1)[0]
        return ""

    @property
    def humans(self) -> List[str]:
        """Twitter handles of filmmakers"""
        handles = []
        with (Path(__file__).parent.parent / "data/handles.json").open("r") as handles_fd:
            handle_map = json.load(handles_fd)
        for name, handle in handle_map.items():
            if name.lower() in self.excerpt.lower():
                handles.append(handle)
        return handles

class Films:
    """Factory to create films more efficiently"""

    def __init__(self) -> None:
        self._raw_films = self._film_list()

    @staticmethod
    def _film_list() -> list:
        """Data from http://firehousefilmcontest.com/?json=1. Don't pull
            as quality is often bad"""
        with (Path(__file__).parent.parent / "data/films.json").open("r") as film_fd:
            return json.load(film_fd)["posts"]

    def get_film(self, max_length: int = 200) -> Film:
        """Get a random film subject to constraint"""
        film = Film(random.choice(self._raw_films))
        if len(film.tweet) <= max_length:
            return film
        return self.get_film()

def no_html(text: str) -> str:
    """Helper to strip HTML from strings"""
    return re.sub("<[^<]+?>", "", text)
