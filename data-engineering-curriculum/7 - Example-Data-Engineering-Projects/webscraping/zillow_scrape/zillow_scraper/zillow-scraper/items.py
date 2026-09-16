import json
from typing import Optional, List, Dict
from dataclasses import dataclass, asdict


@dataclass
class Property:
    _id: str
    price: int
    address: str
    lat: Optional[float]
    lon: Optional[float]
    zipcode: Optional[str]
    url: str
    details: List[str]
    days_on_zillow: Optional[int]
    json: Optional[Dict]

    def to_json(self):
        return json.dumps(asdict(self))
