#!/usr/bin/env python3
"""
Standardize region labels in the dataset.

Usage:
  python standardize_regions.py --in atlas_snp_master_enriched_location.csv \
    --out atlas_snp_master_enriched_location_regions.csv

Optional:
  --mapping path/to/custom_region_map.json
"""

import argparse
import json
import logging
import os
from typing import Dict, Tuple

import pandas as pd


DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_IN = "atlas_snp_master_enriched_location.csv"
DEFAULT_OUT = "final.csv"


CANONICAL_REGIONS = {
    "africa": "Africa",
    "asia": "Asia",
    "apac": "APAC",
    "europe": "Europe",
    "north america": "North America",
    "latin america": "Latin America",
    "middle east": "Middle East",
    "oceania": "Oceania",
    "global": "Global",
}


DEFAULT_MAP = {
    "asia and the pacific": "APAC",
    "asia and pacific": "APAC",
    "asia-pacific": "APAC",
    "apac": "APAC",
    "europe and central asia": "Europe",
    "central and eastern europe": "Europe",
    "western europe": "Europe",
    "eastern europe": "Europe",
    "europe": "Europe",
    "canada": "North America",
    "united states": "North America",
    "united states of america": "North America",
    "usa": "North America",
    "u.s.": "North America",
    "u.s.a.": "North America",
    "us": "North America",
    "north america": "North America",
    "latin america and caribbean": "Latin America",
    "latin america": "Latin America",
    "caribbean": "Latin America",
    "south america": "Latin America",
    "central america": "Latin America",
    "asia": "Asia",
    "east asia": "Asia",
    "south asia": "Asia",
    "southeast asia": "Asia",
    "east asia and pacific": "Asia",
    "sub-saharan africa": "Africa",
    "africa": "Africa",
    "middle east and north africa": "Middle East",
    "middle east": "Middle East",
    "mena": "Middle East",
    "australia and new zealand": "Oceania",
    "australia": "Oceania",
    "new zealand": "Oceania",
    "pacific": "Oceania",
    "oceania": "Oceania",
    "global": "Global",
    "worldwide": "Global",
}

US_STATE_CODES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA",
    "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
    "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
    "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY",
    "DC",
}

US_STATE_NAMES = {
    "alabama", "alaska", "arizona", "arkansas", "california", "colorado",
    "connecticut", "delaware", "florida", "georgia", "hawaii", "idaho",
    "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana",
    "maine", "maryland", "massachusetts", "michigan", "minnesota",
    "mississippi", "missouri", "montana", "nebraska", "nevada",
    "new hampshire", "new jersey", "new mexico", "new york",
    "north carolina", "north dakota", "ohio", "oklahoma", "oregon",
    "pennsylvania", "rhode island", "south carolina", "south dakota",
    "tennessee", "texas", "utah", "vermont", "virginia", "washington",
    "west virginia", "wisconsin", "wyoming", "district of columbia",
}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Standardize region labels.")
    parser.add_argument("--in", dest="in_path", default=DEFAULT_IN, help="Input CSV file.")
    parser.add_argument("--out", dest="out_path", default=DEFAULT_OUT, help="Output CSV file.")
    parser.add_argument(
        "--mapping",
        dest="mapping_path",
        default=None,
        help="Optional JSON mapping file (case-insensitive exact matches).",
    )
    parser.add_argument(
        "--unknown",
        dest="unknown_value",
        default="",
        help="Value to use when no mapping is found (default: empty).",
    )
    parser.add_argument(
        "--log-level",
        default=DEFAULT_LOG_LEVEL,
        help="Logging level (DEBUG, INFO, WARNING, ERROR).",
    )
    return parser.parse_args()


def _load_mapping(path: str) -> Dict[str, str]:
    with open(path, "r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Mapping file must be a JSON object of {string: string}.")
    return {str(k).strip().lower(): str(v).strip() for k, v in data.items()}


def _standardize_region(
    region: str,
    exact_map: Dict[str, str],
    unknown_value: str,
) -> Tuple[str, bool]:
    cleaned = (region or "").strip()
    if not cleaned:
        return unknown_value, cleaned != unknown_value
    lowered = cleaned.lower()

    if lowered in exact_map:
        mapped = exact_map[lowered]
        return mapped, mapped != cleaned

    if "apac" in lowered:
        return CANONICAL_REGIONS["apac"], True

    if "global" in lowered or "world" in lowered:
        return CANONICAL_REGIONS["global"], True

    if "middle east" in lowered or "mena" in lowered:
        return CANONICAL_REGIONS["middle east"], True

    if "africa" in lowered:
        return CANONICAL_REGIONS["africa"], True

    if "latin" in lowered or "caribbean" in lowered:
        return CANONICAL_REGIONS["latin america"], True

    if "north america" in lowered:
        return CANONICAL_REGIONS["north america"], True

    if "east asia" in lowered:
        return CANONICAL_REGIONS["apac"], True

    if "europe" in lowered:
        return CANONICAL_REGIONS["europe"], True

    if "oceania" in lowered or "pacific" in lowered or "australia" in lowered or "new zealand" in lowered:
        return CANONICAL_REGIONS["apac"], True

    if "asia" in lowered:
        return CANONICAL_REGIONS["asia"], True

    return unknown_value, cleaned != unknown_value


def _is_us_row(row: Dict[str, str]) -> bool:
    country = str(row.get("country") or "").strip().lower()
    if country in {"united states", "united states of america", "usa", "us", "u.s.", "u.s.a.", "america"}:
        return True

    location = str(row.get("location") or "").strip().lower()
    if "united states" in location or ", usa" in location or ", us" in location:
        return True

    state_province = str(row.get("state_province") or "").strip()
    if state_province.upper() in US_STATE_CODES:
        return True
    if state_province.lower() in US_STATE_NAMES:
        return True

    return False


def _is_canada_row(row: Dict[str, str]) -> bool:
    country = str(row.get("country") or "").strip().lower()
    if country in {"canada", "ca"}:
        return True

    location = str(row.get("location") or "").strip().lower()
    if ", canada" in location or location.endswith(" canada"):
        return True

    return False


def main() -> None:
    args = _parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )

    if not os.path.exists(args.in_path):
        raise FileNotFoundError(f"Input file not found: {args.in_path}")

    exact_map = dict(DEFAULT_MAP)
    if args.mapping_path:
        exact_map.update(_load_mapping(args.mapping_path))

    df = pd.read_csv(args.in_path, dtype=str).fillna("")
    if "region" not in df.columns:
        raise ValueError("Input CSV must include a 'region' column.")

    logging.info("Loaded %s rows from %s", len(df), args.in_path)

    updated = 0
    unchanged = 0
    missing = 0

    new_regions = []
    for _, row in df.iterrows():
        value = row.get("region", "")
        standardized, changed = _standardize_region(value, exact_map, args.unknown_value)
        if not standardized and _is_us_row(row):
            standardized = CANONICAL_REGIONS["north america"]
            changed = True
        if not standardized and _is_canada_row(row):
            standardized = CANONICAL_REGIONS["north america"]
            changed = True
        new_regions.append(standardized)
        if (value or "").strip() == "":
            missing += 1
        if changed:
            updated += 1
        else:
            unchanged += 1

    df["region"] = new_regions
    df.to_csv(args.out_path, index=False)

    logging.info("Rows with missing region before standardization: %s", missing)
    logging.info("Regions updated: %s", updated)
    logging.info("Regions unchanged: %s", unchanged)
    logging.info("Wrote %s", args.out_path)


if __name__ == "__main__":
    main()
