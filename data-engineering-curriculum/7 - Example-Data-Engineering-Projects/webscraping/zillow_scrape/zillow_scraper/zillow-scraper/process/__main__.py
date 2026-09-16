import sys
import re
from typing import Optional, Tuple, List

import numpy as np
import pandas as pd
from geopy.distance import distance

date = sys.argv[1]

df = pd.read_json(f"raw_data/{date}.json")

# Get latitude and longitude for rows where it isn't already populated.
def extract_ll_from_id(_id: str) -> Tuple[Optional[float], Optional[float]]:
    """
    It seems like many properties that don't have lat/lon have an ID that
    contains their lat/lon.
    """
    try:
        s = _id.lstrip("zpid_")
        lat, lon = s.split("-", 1)
        lat = float(lat)
        lon = float(lon)
        return lat, lon
    except:
        return None, None


no_lat = df.lat.isna()
new_lats = df.loc[no_lat, "_id"].apply(lambda _id: pd.Series(extract_ll_from_id(_id)))
df.loc[no_lat, "lat"] = new_lats[0]
df.loc[no_lat, "lon"] = new_lats[1]

# Certain links are relative -- make them absolute.
prefix = "https://www.zillow.com"
df["url"] = np.where(df.url.str.startswith("http"), df["url"], prefix + df["url"])

# Convert the "details" field into columns where possible.
bed_pattern = re.compile(r"(\d+) bds?")
bath_pattern = re.compile(r"(\d+(\.\d+)?) ba")
sqft_pattern = re.compile(r"(\d+(,\d+)?) sqft")


def extract_bed_bath_sqft(
    details: List,
) -> Tuple[Optional[float], Optional[float], Optional[float]]:
    beds = baths = sqft = None
    for element in details:
        if m := bed_pattern.search(element):
            beds = float(m.group(1))
        elif m := bath_pattern.search(element):
            baths = float(m.group(1))
        elif m := sqft_pattern.search(element):
            sqft = m.group(1).replace(",", "")
            sqft = int(sqft)
    return beds, baths, sqft


detail_cols = df.details.apply(lambda d: pd.Series(extract_bed_bath_sqft(d)))
df["beds"] = detail_cols[0]
df["baths"] = detail_cols[1]
df["sqft"] = detail_cols[2]
df = df.drop("details", axis=1)

# Is the listing for a building or unit?
df["type"] = np.where(
    df.url.str.startswith("https://www.zillow.com/b/"), "building", "unit"
)

# Keep only unique rows.
df = df.drop("json", axis=1)
df = df.drop_duplicates()

# Now that the rows are unique, we can set the index to the property ID.
df = df.set_index("_id")

# How far is this place from the Old Town location I want?
old_town_coords = (41.910322, -87.632164)


def from_ot(row):
    if pd.notnull(row["lat"]) and pd.notnull(row["lon"]):
        location = row["lat"], row["lon"]
        return distance(old_town_coords, location).miles
    else:
        return None


df["old_town_distance"] = df.apply(from_ot, axis=1)


df.to_json(f"clean_data/{date}.json")
