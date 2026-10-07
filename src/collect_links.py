#!/usr/bin/env python3
"""Collect the Links: build the list of pages to scrape.

The Meeple & Mug game library is split across 12 catalog pages. Before you
can scrape every page, you need the full URL of each one, and the full URL of
each game's detail page.
"""

import re

import requests
from bs4 import BeautifulSoup

# Toolkit (from class): don't change
BASE = "https://moden-coding.github.io/scrape-practice-site/catalog/"


def fetch_and_save(url, path):
    """Download the page at url, save it to path, and return the status code."""
    resp = requests.get(url, timeout=20)
    resp.encoding = "utf-8"
    with open(path, "w", encoding="utf-8") as f:
        f.write(resp.text)
    return resp.status_code


def load_soup(path):
    """Open a saved HTML file and return it as a BeautifulSoup object."""
    with open(path, encoding="utf-8") as f:
        return BeautifulSoup(f.read(), "html.parser")


# Your code below


def page_urls(soup):
    """Return a list of the full URLs of all 12 catalog pages, with no duplicates."""
    pass


def game_urls(soup):
    """Return a list of the full URLs of the game detail pages on this page, with no duplicates."""
    pass


def main():
    """Fetch catalog page 1, save it, and print how many page and game URLs were found."""
    status = fetch_and_save(BASE + "page-1.html", "page-1.html")
    print("Status:", status)
    soup = load_soup("page-1.html")

    pages = page_urls(soup)
    games = game_urls(soup)
    print("Found", len(pages), "page URLs")
    print(pages[:3])
    print("Found", len(games), "game URLs")
    print(games[:3])


if __name__ == "__main__":
    main()
