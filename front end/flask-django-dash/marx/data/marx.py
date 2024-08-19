import pandas as pd
import wikipedia
from bs4 import BeautifulSoup as soup
import functools
from dataclasses import dataclass
from knowledge import EntityType
from config import skip, required
import traceback
import re
import csv


@dataclass
class record:
    direction: str
    url: str
    philosopher: str
    connection: str


class Philosopher(wikipedia.wikipedia.WikipediaPage):
    """Class representing philosopher"""

    def __init__(self, name):
        super(wikipedia.wikipedia.WikipediaPage).__init__()
        self.BASE_URL = "https://en.wikipedia.org"
        self.name = name
        self.regex = re.compile("[^a-zA-Z ]")
        self._set_attrs()

    def __repr__(self):
        return str("name: {}".format(self.name))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
            return False
        return True

    @property
    def _url(self):
        if not hasattr(self, "wiki_page"):
            self.get_page
        return self.wiki_page.url

    @property
    def _links(self):
        if not hasattr(self, "wiki_page"):
            self.get_page
        return self.wiki_page.links

    @property
    def query_wiki(self):
        if hasattr(self, "matches"):
            return self.matches[0]
        self.matches = wikipedia.search(self.name)
        if self.matches:
            return self.matches[0]
        self.matches = None
        return self.matches

    @property
    def get_page(self):
        if not hasattr(self, "matches"):
            self.query_wiki
        if self.matches:
            if not hasattr(self, "wiki_page"):
                try:
                    self.wiki_page = wikipedia.page(self.query_wiki)
                except wikipedia.PageError:
                    print("No page for: {}".format(self.query_wiki))
                    self.wiki_page = None
                    pass
                return self.wiki_page
        else:
            self.wiki_page = None
            return self.wiki_page

    @property
    def get_html(self):
        if not hasattr(self, "wiki_page"):
            self.get_page
        if not hasattr(self, "soup"):
            if not self.wiki_page:
                self.soup = None
                return self.soup
            self.soup = soup(self.wiki_page.html(), "html.parser")
        else:
            self.soup = None
        return self.soup

    @property
    def get_influences(self):
        if not hasattr(self, "soup"):
            self.get_html
        if not self.soup:
            self.influences = None
            return self.influences
        influences = self.search_for_influences()
        if not influences:
            self.influences = "No table for: {}".format(self.name)
            return self.influences
        candidates = {inf.find_previous().text: inf for inf in influences}
        self.influences = candidates
        return self.influences

    def _set_attrs(self):
        self.get_influences

    def strip_chars(self, name):
        regex = re.compile("[^a-zA-Z ]")
        return regex.sub("", name)

    def search_for_influences(self):
        list_of_influences = self.soup.find_all("ul", class_="mw-collapsible-content")
        if list_of_influences:
            return list_of_influences
        table = self.soup.find_all("table", class_="infobox biography vcard")
        if not table:
            return None
        rows = table[0].find_all("tr")
        for row in rows:
            header = row.find("th")
            if header:
                if "influences" in header.text.lower():
                    list_of_influences = row.find_all("ul")
                    return list_of_influences
        return None

    def parse_influences(self):
        if isinstance(self.influences, str):
            return self.influences
        records = []
        for k, v in self.influences.items():
            if k not in ["Influences", "Influenced"]:
                continue
            for a in v.find_all("a"):
                if all(x in a.__dict__["attrs"].keys() for x in ["href", "title"]):
                    candidate = self.strip_chars(a["title"])
                    entity = EntityType(candidate)
                    if not entity.parse_results():
                        continue
                    records.append(
                        record(
                            direction=k,
                            url=self.BASE_URL + a["href"],
                            philosopher=candidate,
                            connection=self.name,
                        )
                    )
        return records


class cache(dict):
    def __init__(self, func):
        self.func = func

    def __call__(self, *args):
        return self[args]

    def __missing__(self, key):
        result = self[key] = self.func(*key)
        return result


def create_network(required):
    store, no_good = [], []

    def construct_network(required, depth=2):
        if depth < 0:
            return
        for philosopher in required:
            print(philosopher)
            results = process(philosopher)
            if not results or isinstance(results, str):
                no_good.append(results)
                continue
            store.append(results)
            search_for = [result.philosopher for result in results]
            depth -= 1
            construct_network(search_for, depth)

    construct_network(required)
    return store


@cache
def process(philosopher):
    with Philosopher(philosopher) as phil:
        if not phil.wiki_page:
            return "No results for: {}".format(phil)
        records = phil.parse_influences()
    return records
