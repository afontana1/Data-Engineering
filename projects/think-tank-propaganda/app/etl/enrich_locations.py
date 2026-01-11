#!/usr/bin/env python3
"""
Enrich missing location values using the OpenAI API.

Usage:
  python enrich_locations.py --in atlas_spn_master.csv --out atlas_spn_master_enriched.csv
"""

import argparse
import asyncio
import logging
import os
from typing import Dict, List, Optional

import pandas as pd
from openai import AsyncOpenAI


OPEN_AI_KEY = ""
DEFAULT_MODEL = "gpt-4o-mini"
DEFAULT_LOG_LEVEL = "INFO"
DEFAULT_BATCH_SIZE = 50
DEFAULT_CONCURRENCY = 8


def _build_row_context(row: Dict[str, str]) -> str:
    parts = []
    for key in [
        "institution",
        "org_name",
        "region",
        "city",
        "state_province",
        "country",
        "website",
        "sourcewatch_page_url",
    ]:
        value = (row.get(key) or "").strip()
        if value:
            parts.append(f"{key}: {value}")
    return "\n".join(parts)


async def _openai_chat(client: AsyncOpenAI, messages: List[Dict[str, str]], model: str) -> str:
    resp = await client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.2,
    )
    return resp.choices[0].message.content.strip()


async def _propose_location(client: AsyncOpenAI, row: Dict[str, str], model: str) -> str:
    context = _build_row_context(row)
    prompt = (
        "Given the organization details, infer the most specific location string to fill the "
        "'location' field. Use a concise format like 'City, State/Province, Country' or "
        "'State/Province, Country' if city is unknown. Return only the location string."
    )
    messages = [
        {"role": "system", "content": "You infer missing location fields for datasets."},
        {"role": "user", "content": f"{prompt}\n\n{context}"},
    ]
    return await _openai_chat(client, messages, model)


async def _verify_location(
    client: AsyncOpenAI, row: Dict[str, str], candidate: str, model: str
) -> bool:
    context = _build_row_context(row)
    prompt = (
        "You are an adversarial verifier. Given the organization details and a proposed location, "
        "decide if the location is correct. Reply with a single word: TRUE or FALSE."
    )
    messages = [
        {"role": "system", "content": "You verify location assignments."},
        {
            "role": "user",
            "content": f"{prompt}\n\nProposed location: {candidate}\n\n{context}",
        },
    ]
    verdict = (await _openai_chat(client, messages, model)).upper()
    return verdict == "TRUE"


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Enrich missing location values.")
    parser.add_argument(
        "--in",
        dest="in_path",
        default="atlas_spn_master.csv",
        help="Input CSV file.",
    )
    parser.add_argument(
        "--out",
        dest="out_path",
        default=None,
        help="Output CSV file (defaults to input with _enriched suffix).",
    )
    parser.add_argument("--model", default=DEFAULT_MODEL, help="OpenAI model id.")
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.2,
        help="Seconds to sleep between API calls.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Number of rows to process per batch.",
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


def _resolve_out_path(in_path: str, out_path: Optional[str]) -> str:
    if out_path:
        return out_path
    base, ext = os.path.splitext(in_path)
    return f"{base}_enriched{ext or '.csv'}"


async def _process_row(
    client: AsyncOpenAI,
    row: Dict[str, str],
    model: str,
    sleep_seconds: float,
    idx: int,
    sem: asyncio.Semaphore,
) -> Optional[str]:
    async with sem:
        logging.info("Row %s: proposing location for org=%s", idx, row.get("org_name"))
        candidate = await _propose_location(client, row, model)
        logging.debug("Row %s: candidate location=%s", idx, candidate)
        await asyncio.sleep(sleep_seconds)
        if not candidate:
            logging.warning("Row %s: no candidate location", idx)
            return None
        logging.info("Row %s: verifying candidate", idx)
        if await _verify_location(client, row, candidate, model):
            logging.info("Row %s: accepted location=%s", idx, candidate)
            return candidate
        logging.warning("Row %s: rejected location=%s", idx, candidate)
        await asyncio.sleep(sleep_seconds)
        return None


async def _process_batch(
    client: AsyncOpenAI,
    batch_rows: List[Dict[str, str]],
    model: str,
    sleep_seconds: float,
    start_idx: int,
    concurrency: int,
) -> List[Optional[str]]:
    sem = asyncio.Semaphore(concurrency)
    tasks = []
    for offset, row in enumerate(batch_rows):
        idx = start_idx + offset
        tasks.append(
            _process_row(client, row, model, sleep_seconds, idx, sem)
        )
    return await asyncio.gather(*tasks)


async def main_async() -> None:
    args = _parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        format="%(asctime)s %(levelname)s %(message)s",
    )
    api_key = os.getenv("OPENAI_API_KEY", OPEN_AI_KEY)
    out_path = _resolve_out_path(args.in_path, args.out_path)
    client = AsyncOpenAI(api_key=api_key)

    df = pd.read_csv(args.in_path, dtype=str).fillna("")
    if "location" not in df.columns:
        raise ValueError("Input CSV must include a 'location' column.")

    missing_mask = df["location"].str.strip() == ""
    missing_df = df[missing_mask].copy()
    total_missing = len(missing_df)
    logging.info("Loaded %s rows from %s", len(df), args.in_path)
    logging.info("Rows missing location: %s", total_missing)
    if total_missing == 0:
        df.to_csv(out_path, index=False)
        logging.info("No missing locations. Wrote %s", out_path)
        return

    rows = missing_df.to_dict(orient="records")
    batch_size = max(1, args.batch_size)
    cursor = 0
    while cursor < total_missing:
        batch = rows[cursor : cursor + batch_size]
        results = await _process_batch(
            client,
            batch,
            args.model,
            args.sleep,
            cursor + 1,
            args.concurrency,
        )
        for i, candidate in enumerate(results):
            if candidate:
                missing_df.iloc[cursor + i, missing_df.columns.get_loc("location")] = candidate
        cursor += batch_size

    df.loc[missing_mask, "location"] = missing_df["location"]
    df.to_csv(out_path, index=False)
    logging.info("Wrote %s", out_path)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
