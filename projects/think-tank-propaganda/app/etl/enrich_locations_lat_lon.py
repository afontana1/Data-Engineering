#!/usr/bin/env python3
"""
Enrich location values with latitude and longitude using the OpenAI API.

Usage:
  python enrich_locations_lat_lon.py --in atlas_spn_master_enriched.csv \
    --out atlas_snp_master_enriched_location.csv
"""

import argparse
import asyncio
import json
import logging
import os
import re
from typing import Dict, List, Optional, Tuple

import pandas as pd
from openai import AsyncOpenAI

OPEN_AI_KEY = ""
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_SLEEP = 0.2
DEFAULT_CONCURRENCY = 8
DEFAULT_OUT = "atlas_snp_master_enriched_location.csv"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Enrich location values with latitude and longitude."
    )
    parser.add_argument(
        "--in",
        dest="in_path",
        default="atlas_spn_master_enriched.csv",
        help="Input CSV file.",
    )
    parser.add_argument(
        "--out",
        dest="out_path",
        default=DEFAULT_OUT,
        help="Output CSV file.",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model id.")
    parser.add_argument(
        "--sleep",
        type=float,
        default=DEFAULT_SLEEP,
        help="Seconds to sleep between API calls.",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=DEFAULT_CONCURRENCY,
        help="Maximum concurrent OpenAI requests.",
    )
    parser.add_argument(
        "--log-level",
        default=DEFAULT_LOG_LEVEL,
        help="Logging level (DEBUG, INFO, WARNING, ERROR).",
    )
    return parser.parse_args()


async def _openai_chat(client: AsyncOpenAI, messages: List[Dict[str, str]], model: str) -> str:
    resp = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0,
    )
    return resp.choices[0].message.content.strip()


def _extract_lat_lon(text: str) -> Tuple[Optional[float], Optional[float]]:
    try:
        payload = json.loads(text)
        lat = payload.get("lat")
        lon = payload.get("lon")
        if lat is None or lon is None:
            return None, None
        return float(lat), float(lon)
    except (json.JSONDecodeError, ValueError, TypeError, AttributeError):
        pass

    numbers = re.findall(r"-?\d+\.\d+", text)
    if len(numbers) >= 2:
        try:
            lat = float(numbers[0])
            lon = float(numbers[1])
            return lat, lon
        except ValueError:
            return None, None
    return None, None


async def _geocode_location(
    client: AsyncOpenAI,
    location: str,
    model: str,
    sleep_seconds: float,
    sem: asyncio.Semaphore,
) -> Tuple[Optional[float], Optional[float]]:
    async with sem:
        prompt = (
            "Given the location string, return JSON with numeric lat and lon in decimal degrees. "
            "Use null if you cannot determine the coordinates. Return only JSON."
        )
        messages = [
            {"role": "system", "content": "You convert locations to latitude/longitude."},
            {"role": "user", "content": f"{prompt}\n\nLocation: {location}"},
        ]
        response = await _openai_chat(client, messages, model)
        lat, lon = _extract_lat_lon(response)
        await asyncio.sleep(sleep_seconds)
        return lat, lon


def _build_region_context(row: Dict[str, str]) -> str:
    parts = []
    for key in [
        "institution",
        "org_name",
        "location",
        "city",
        "state_province",
        "country",
        "lat",
        "lon",
        "website",
        "sourcewatch_page_url",
    ]:
        raw_value = row.get(key)
        if raw_value is None:
            continue
        value = str(raw_value).strip()
        if value:
            parts.append(f"{key}: {value}")
    return "\n".join(parts)


def _normalize_region(text: str) -> Optional[str]:
    if text is None:
        return None
    cleaned = text.strip()
    if not cleaned:
        return None
    lowered = cleaned.lower()
    if lowered in {"null", "none", "unknown", "n/a", "na"}:
        return None
    return cleaned


async def _infer_region(
    client: AsyncOpenAI,
    row: Dict[str, str],
    model: str,
    sleep_seconds: float,
    sem: asyncio.Semaphore,
) -> Optional[str]:
    async with sem:
        context = _build_region_context(row)
        prompt = (
            "Given the record fields, infer the most likely geographic region for the 'region' field. "
            "Use labels like North America, Latin America, Europe, Asia, Africa, Oceania, Middle East, "
            "or Global. Return only the region string or null if it cannot be inferred."
        )
        messages = [
            {"role": "system", "content": "You infer region labels for dataset records."},
            {"role": "user", "content": f"{prompt}\n\n{context}"},
        ]
        response = await _openai_chat(client, messages, model)
        await asyncio.sleep(sleep_seconds)
        return _normalize_region(response)


async def _process_locations(
    client: AsyncOpenAI,
    locations: List[str],
    model: str,
    sleep_seconds: float,
    concurrency: int,
) -> Dict[str, Tuple[Optional[float], Optional[float]]]:
    sem = asyncio.Semaphore(concurrency)
    tasks = []
    for location in locations:
        tasks.append(_geocode_location(client, location, model, sleep_seconds, sem))
    results = await asyncio.gather(*tasks)
    return dict(zip(locations, results))


async def _process_regions(
    client: AsyncOpenAI,
    rows: List[Tuple[int, Dict[str, str]]],
    model: str,
    sleep_seconds: float,
    concurrency: int,
) -> Dict[int, Optional[str]]:
    sem = asyncio.Semaphore(concurrency)
    tasks = []
    indices = []
    for idx, row in rows:
        indices.append(idx)
        tasks.append(_infer_region(client, row, model, sleep_seconds, sem))
    results = await asyncio.gather(*tasks)
    return dict(zip(indices, results))


async def main_async() -> None:
    args = _parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )

    api_key = os.getenv("OPENAI_API_KEY", OPEN_AI_KEY)
    client = AsyncOpenAI(api_key=api_key)

    df = pd.read_csv(args.in_path, dtype=str).fillna("")
    if "location" not in df.columns:
        raise ValueError("Input CSV must include a 'location' column.")
    logging.info("Loaded %s rows from %s", len(df), args.in_path)

    if "lat" not in df.columns:
        df["lat"] = ""
    if "lon" not in df.columns:
        df["lon"] = ""
    if "region" not in df.columns:
        df["region"] = ""

    location_map: Dict[str, List[int]] = {}
    rows_missing_coords = 0
    for idx, row in df.iterrows():
        location = (row.get("location") or "").strip()
        if not location:
            continue
        existing_lat = (row.get("lat") or "").strip()
        existing_lon = (row.get("lon") or "").strip()
        if existing_lat and existing_lon:
            continue
        rows_missing_coords += 1
        location_map.setdefault(location, []).append(idx)

    unique_locations = list(location_map.keys())
    logging.info(
        "Rows missing lat/lon: %s (unique locations=%s)",
        rows_missing_coords,
        len(unique_locations),
    )
    if not unique_locations:
        df.to_csv(args.out_path, index=False)
        logging.info("No locations to geocode. Wrote %s", args.out_path)
        return

    results = await _process_locations(
        client,
        unique_locations,
        args.model,
        args.sleep,
        args.concurrency,
    )

    filled = 0
    failed_locations: List[str] = []
    for location, indices in location_map.items():
        lat, lon = results.get(location, (None, None))
        if lat is None or lon is None:
            failed_locations.append(location)
            continue
        for idx in indices:
            df.at[idx, "lat"] = lat
            df.at[idx, "lon"] = lon
            filled += 1
    if failed_locations:
        logging.warning(
            "Failed to resolve %s unique locations (example: %s)",
            len(failed_locations),
            failed_locations[0],
        )
        logging.debug("Unresolved locations: %s", failed_locations)
    logging.info("Filled lat/lon for %s rows", filled)

    region_rows: List[Tuple[int, Dict[str, str]]] = []
    for idx, row in df.iterrows():
        region_value = (row.get("region") or "").strip()
        if region_value:
            continue
        region_rows.append((idx, row.to_dict()))

    if region_rows:
        logging.info("Rows missing region: %s", len(region_rows))
        region_results = await _process_regions(
            client,
            region_rows,
            args.model,
            args.sleep,
            args.concurrency,
        )
        region_filled = 0
        region_failed = 0
        for idx, region in region_results.items():
            if region:
                df.at[idx, "region"] = region
                region_filled += 1
            else:
                region_failed += 1
        logging.info(
            "Filled %s region values (%s unresolved)",
            region_filled,
            region_failed,
        )

    df.to_csv(args.out_path, index=False)
    logging.info("Wrote %s", args.out_path)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
