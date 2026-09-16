import requests
from bs4 import BeautifulSoup
import csv
import json


class ZillowScraper:
    results = []

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "en-US,en;q=0.9",
        "cache-control": "no-cache",
        "pragma": "no-cache",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/75.0.3770.142 Chrome/75.0.3770.142 Safari/537.36",
    }

    def fetch(self, url, params):
        print("HTTP GET request to URL: %s" % url, end="")
        res = requests.get(url, params=params, headers=self.headers)
        print(" | Status code: %s" % res.status_code)
        print(res.text)

        return res

    def save_response(self, res):
        with open("res.html", "w") as html_file:
            html_file.write(res)

    def load_response(self):
        html = ""

        with open("res.html", "r") as html_file:
            for line in html_file:
                html += line

        return html

    def parse(self, html):
        content = BeautifulSoup(html, "lxml")
        cards = content.findAll("article", {"class": "list-card"})

        for card in cards:
            # try to extract image
            try:
                image = card.find("div", {"class": "list-card-top"}).find("img")["src"]
            except:
                image = "N/A"

            # extract items
            items = {
                "url": card.find("a", {"class": "list-card-link"})["href"],
                "details": [
                    price.text
                    for price in card.find(
                        "ul", {"class": "list-card-details"}
                    ).find_all("li")
                ],
                "address": card.find("address", {"class": "list-card-addr"}).text,
                "image": image,
            }

            # try to extract price if not extracted yet
            try:
                items["price"] = card.find("div", {"class": "list-card-price"}).text
            except:
                pass

            # append scraped items to results list
            self.results.append(items)
            print(json.dumps(items, indent=2))

    def to_json(self):
        with open("zillow_rent.json", "w") as f:
            f.write(json.dumps(self.results, indent=2))

    def run(self):
        for page in range(1, 5):
            params = {
                "searchQueryState": '{"pagination":{"currentPage":%s},"mapBounds":{"west":-84.69197781640625,"east":-84.26900418359375,"south":33.61815664689875,"north":33.91554940040142},"regionSelection":[{"regionId":37211,"regionType":6}],"isMapVisible":true,"mapZoom":11,"filterState":{"isForSaleByAgent":{"value":false},"isForSaleByOwner":{"value":false},"isNewConstruction":{"value":false},"isForSaleForeclosure":{"value":false},"isComingSoon":{"value":false},"isAuction":{"value":false},"isPreMarketForeclosure":{"value":false},"isPreMarketPreForeclosure":{"value":false},"isForRent":{"value":true}},"isListVisible":true}'
                % str(page)
            }

            res = self.fetch("https://www.zillow.com/atlanta-ga/rentals/2_p/?", params)
            self.parse(res.text)

        self.to_json()


if __name__ == "__main__":
    scraper = ZillowScraper()
    scraper.run()
