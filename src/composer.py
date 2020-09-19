#!/usr/bin/env python3
"""Compose tweets about Firehouse films"""

import re
import json
import html
import random
from pathlib import Path
from typing import List, Dict, Any

from bs4 import BeautifulSoup

class Film:
    """Film metadata"""

    def __init__(self, data: Dict[str, Any]) -> None:
        self.title = html.unescape(data["title"])
        self.categories = data["categories"]
        self.firehouse_no = self.categories[0]["title"].split()[0][1:]
        self.url = data["url"].split("http://", maxsplit=1)[1]
        self.excerpt = html.unescape(no_html(data["excerpt"])).strip()
        self.content = data["content"]
        #self.firehouse_name = unescape(" ".join(data["categories"][0]["title"].split()[1:]))
        #self.img_url = data["thumbnail_images"]["large"]["url"]

    def __len__(self) -> int:
        return len(self.text()) - len(self.url) - len(self.video_url) + 2 * 23

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

    def text(self) -> str:
        """Compose a tweet about a film"""
        tweet = ""
        if self.awards:
            tweet = "Winner of " + ", ".join(self.awards) + " in "
        else:
            tweet = "From "
        tweet += f"Firehouse {self.firehouse_no}, “{self.title}”"
        if self.humans:
            tweet += " by " + ", ".join(["@" + human for human in self.humans])
        tweet += f": {self.url}. {self.video_url}"
        return tweet

class Films:
    """Factory to create films more efficiently"""

    def __init__(self) -> None:
        self._raw_films = self._film_list()
        self._position = 0
        self._end = len(self._raw_films) - 1

    def __iter__(self) -> "Films":
        return self

    def __next__(self) -> Film:
        if self._position >= self._end:
            raise StopIteration
        self._position += 1
        return Film(self._raw_films[self._position])

    @staticmethod
    def _film_list() -> list:
        """Data from http://firehousefilmcontest.com/?json=1"""
        with (Path(__file__).parent.parent / "data/films.json").open("r") as film_fd:
            return json.load(film_fd)["posts"]

    def choice(self, max_length: int = 200) -> Film:
        """Get a random film subject to length constraint"""
        film = Film(random.choice(self._raw_films))
        if len(film.text()) <= max_length:
            return film
        return self.choice()

def no_html(text: str) -> str:
    """Helper to strip HTML from strings"""
    return re.sub("<[^<]+?>", "", text)

def main() -> None:
    """Entry point"""
    films = Films()
    for film in films:
        print(film.text(), end="\n\n")

if __name__ == "__main__":
    main()
