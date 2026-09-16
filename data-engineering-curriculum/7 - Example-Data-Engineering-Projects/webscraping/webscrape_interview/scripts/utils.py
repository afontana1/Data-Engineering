"""
Helper functions:
- validate URL before making request based on regex rules
- make request to server, returning response object or indicator of an error
"""
import requests
import re
import json

params = {"products": "ABS", "regions": "USOA"}
BASE_URL = "https://finsight.com/product/us/abs/ee"


def is_valid_url(url):
    """Validate the URL.
    Args:
        url (String): candidate URL
    Return:
        URL or None: validated URL or None
    """
    regex = re.compile(
        r"^https?://"  # http:// or https://
        r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain
        r"localhost|"  # localhost...
        r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # or ip
        r"(?::\d+)?"  # optional port
        r"(?:/?|[/?]\S+)$",
        re.IGNORECASE,
    )
    check_url = regex.search(url)
    if check_url:
        return check_url.group()


def make_request(url, params=None):
    """Make request to external server.
    Args:
        url (string): Candidate URL to target
    Return:
        object (response object) or dict: if successful, return content. If else, return status code.
    """
    if is_valid_url(url):
        response = requests.get(
            url,
            headers={
                "Connection": "close",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
            params=params,
        )
        if not response.status_code != "200":
            return {"URL": url, "status": response.status_code}
        return response
    return url
