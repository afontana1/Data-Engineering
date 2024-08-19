from fastapi import FastAPI

import requests
from bs4 import BeautifulSoup

app = FastAPI()


@app.get("/{asin}")
async def get_data(asin: str):
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"
        }
    )
    resp = session.get(f"https://amazon.co.uk/dp/{asin}")
    if resp.status_code != 200:
        return {"error": f"bad status code {resp.status_code}"}
    soup = BeautifulSoup(resp.text, "html.parser")
    try:
        data = {
            "asin": asin,
            "name": soup.select_one("h1#title").text.strip(),
            "price": soup.select_one("span.a-offscreen").text,
        }
        return {"results": data}
    except KeyError:
        return {"error": "Unable to parse page"}
