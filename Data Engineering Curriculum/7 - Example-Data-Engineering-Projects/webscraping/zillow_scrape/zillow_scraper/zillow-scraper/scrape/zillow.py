from urllib.parse import quote as url_quote
import json
from typing import Any, Dict

import requests


CHI_URL = "https://www.zillow.com/chicago-il/rentals/"
HEADERS = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US,en;q=0.8",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}


def make_query_state(page_num: int = 0) -> Dict[str, Any]:
    # The below reflects page 0 of a search for:
    # - Chicago         - For rent
    # - In-unit laundry - 2+ Bedrooms
    # - Rent: $0-$3000/month
    query_state = {
        "pagination": {},
        "mapBounds": {
            "west": -88.09607811914063,
            "east": -87.36823388085938,
            "south": 41.217142667058575,
            "north": 42.444992337648856,
        },
        "regionSelection": [{"regionId": 17426, "regionType": 6}],
        "isMapVisible": False,
        "filterState": {
            "fsba": {"value": False},
            "fsbo": {"value": False},
            "nc": {"value": False},
            "fore": {"value": False},
            "cmsn": {"value": False},
            "auc": {"value": False},
            "pmf": {"value": False},
            "pf": {"value": False},
            "fr": {"value": True},
            "ah": {"value": True},
            "mf": {"value": False},
            "manu": {"value": False},
            "land": {"value": False},
            # Here begin the params I understand: beds, price, laundry, days on Zillow.
            "beds": {"min": 2},
            "mp": {"max": 3000},
            "price": {"max": 890941},
            "lau": {"value": True},
            "doz": {"value": "7"},
        },
        "isListVisible": True,
    }
    # If we're on a page other than 0, we need to add that to the query.
    if page_num > 0:
        query_state["pagination"] = {"currentPage": page_num}
    return query_state


def get_search_page(session: requests.Session, page_num: int):
    q_state = make_query_state(page_num)
    formatted_q_state = url_quote(json.dumps(q_state))
    formatted_url = f"{CHI_URL}/?searchQueryState={formatted_q_state}"
    response = session.get(formatted_url, headers=HEADERS)
    response.raise_for_status()
    return response.content
