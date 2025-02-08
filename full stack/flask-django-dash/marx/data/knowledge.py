import requests
import config
import json


class EntityType(object):
    """Used to validate that the influence is a person"""

    def __init__(self, query):
        self.query = query
        self.params = {
            "query": query,
            "limit": 10,
            "indent": True,
            "key": config.KNOWLEDGE_GRAPH_API_KEY,
        }
        self.BASE_URL = "https://kgsearch.googleapis.com/v1/entities:search"

    def _make_request(self):
        resp = requests.get(url=self.BASE_URL, params=self.params)
        try:
            resp.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return "Error: {}".format(e)

        return json.loads(resp.content)

    def parse_results(self):
        content = self._make_request()
        if "itemListElement" not in content.keys():
            raise KeyError
        item_list = content.get("itemListElement")
        for items in item_list:
            result = items.get("result", "")
            if not result:
                return None
            entity_types = result.get("@type")
            if "Person" in entity_types:
                return True
        return False


if __name__ == "__main__":
    query = "Frankfurt School"
    entity = EntityType(query)
    print(entity.parse_results())
