import sys
import time
import json
import re
import logging
import datetime as dt
import random
from typing import Optional, Union, Iterable, overload, Literal

import requests
from requests.exceptions import HTTPError
from bs4.element import Tag
from bs4 import BeautifulSoup
import pandas as pd

from ..items import Property
from .zillow import get_search_page


logging.basicConfig(level=logging.DEBUG)


@overload
def property_from_card(card: Tag, suppress_errors: Literal[False] = False) -> Property:
    ...


@overload
def property_from_card(card: Tag, suppress_errors: Literal[True]) -> Optional[Property]:
    ...


def property_from_card(card, suppress_errors=False) -> Property:
    # This just calls the function again, but with errors caught.
    if suppress_errors:
        try:
            return property_from_card(card, suppress_errors=False)
        except Exception as exc:
            logging.warning("Failed to parse property card.")
            return None
    prop_id = card.article.attrs["id"]
    details_card = card.article.find("ul", class_="list-card-details")
    details = [detail.text for detail in details_card.children]
    if daydiv := card.find("div", text=re.compile(r"days? on Zillow")):
        days_on_zillow_str = daydiv.text
        days_on_zillow = re.match(r"(\d+) day", days_on_zillow_str).group(1)  # type: ignore
    else:
        # We might be wrong, but usually if the "days" string isn't found, it's
        # a different string like "1 hour ago" indicating less than a day.
        days_on_zillow = 0
    url = card.find("a", class_="list-card-link").attrs["href"]
    address = card.find("address").text
    # Price text is sometimes "$1,500/mo", "$1,300+ 1bd", and "$1,700 1 bd".
    raw_price = card.find("div", class_="list-card-price").text
    price_str = re.match(r"\$(.*?)(\+?)[\s/]", raw_price).group(1)  # type: ignore
    price = int(price_str.replace(",", ""))
    j_script = card.find("script", {"type": "application/ld+json"})
    j = lat = lon = zipcode = None
    if j_script is not None:
        j = json.loads(j_script.contents[0])
        if "geo" in j:
            lat = j["geo"].get("latitude")
            lon = j["geo"].get("longitude")
        if "address" in j:
            zipcode = j["address"].get("postalCode")
    prop = Property(
        _id=prop_id,
        price=price,
        address=address,
        lat=lat,
        lon=lon,
        zipcode=zipcode,
        url=url,
        details=details,
        days_on_zillow=days_on_zillow,
        json=j,
    )
    logging.info("Successfully parsed property card.")
    return prop


def extract_properties(content: Union[str, bytes]) -> Iterable[Property]:
    soup = BeautifulSoup(content, "html.parser")
    potential_prop_cards = soup.find_all("ul", {"class": {"photo-cards"}})
    if len(potential_prop_cards) == 0:
        logging.info("Found page with zero prop cards")
        return []
    elif len(potential_prop_cards) > 1:
        raise ValueError("Ambiguous situation in parsing -- too many photo-cards")
    else:
        prop_cards = potential_prop_cards[0]
    result = filter(
        lambda x: x is not None,
        (
            property_from_card(card)
            for card in prop_cards.children
            if card.name == "li" and card.article is not None
        ),
    )
    logging.info("Returned generator of properties from page.")
    return result


def get_next_property(session: requests.Session, max_pages: Optional[int] = None):
    page_num = 0
    while True:
        if max_pages and page_num >= max_pages:
            break
        try:
            page = get_search_page(session=session, page_num=page_num)
            logging.info("Successfully fetched new page.")
        except HTTPError:
            # Assume we've hit the end of the results.
            break
        records = extract_properties(page)
        yield from records
        page_num += 1
        # Simulate normal human behavior.
        delay = 12 * random.betavariate(2, 5)
        time.sleep(delay)
        logging.debug(f"Waited {delay} seconds")


if __name__ == "__main__":
    with requests.Session() as session:
        if len(sys.argv) > 1:
            max_pages: Optional[int] = int(sys.argv[1])
        else:
            max_pages = None
        properties = get_next_property(session, max_pages)
        # Originally I thought I could set the DF index to '_id' but it isn't
        # unique, and that breaks the .to_json() call later.
        df = pd.DataFrame(properties)
        today = dt.date.today().strftime("%Y%m%d")
        filename = f"raw_data/{today}.json"
        df.to_json(filename)
        logging.info(f"Wrote data to {filename}")
