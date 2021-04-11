import urllib.request
import requests
from bs4 import BeautifulSoup

import time


BASE_URL = "https://en.wikipedia.org/wiki/"


MIN_TIME_BETWEEN_REQUESTS_SECONDS = 1.0
LAST_REQUEST_TIMESTAMP = 0.0


def is_valid_pagename(href):
    return all([
        href.startswith("/wiki/"),
        not href.startswith("/wiki/File:"),
        not href.startswith("/wiki/Special:"),
        not href.startswith("/wiki/Template:"),
        not href.startswith("/wiki/Template_Talk:"),
        not href.startswith("/wiki/Book:"),
        not href.startswith("/wiki/Wikipedia:"),
        not href.startswith("/wiki/Help:"),
        not href.startswith("/wiki/Portal:"),
        not href.startswith("/wiki/Category:"),
        not href.startswith("/wiki/Talk:"),
        not href.startswith("/wiki/User:"),
        not href.startswith("/wiki/MediaWiki:"),
        not href.startswith("/wiki/Draft:"),
        not href.startswith("/wiki/TimedText:"),
        not href.startswith("/wiki/Module:"),
        not href.startswith("/wiki/Media:")
    ])



def get_links(pagename):
    """returns a set of unique pagenames present in the given page"""
    global LAST_REQUEST_TIMESTAMP

    # wait until enough time has passed
    elapsed = time.time() - LAST_REQUEST_TIMESTAMP
    if elapsed < MIN_TIME_BETWEEN_REQUESTS_SECONDS:
        time.sleep(MIN_TIME_BETWEEN_REQUESTS_SECONDS - elapsed)
    LAST_REQUEST_TIMESTAMP = time.time()

    url = f"{BASE_URL}{pagename}"

    response = requests.get(url)
    soup = BeautifulSoup(
        response.text,
        "html.parser", 
        from_encoding="utf-8"
    )

    links = set()
    for link in soup.find_all('a', href=True):
        href = link["href"]
        if is_valid_pagename(href):
            links.add(href[6:])
    
    return sorted(links)



from pprint import pprint

if __name__ == "__main__":
    res = get_links("Main_Page")
    pprint(list(res))




