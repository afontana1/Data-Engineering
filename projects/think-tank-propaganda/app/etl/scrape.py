#!/usr/bin/env python3
"""
Build a combined dataset of:
  - Atlas Network partners (from DeSmog's Wayback-based 2021 directory XLSX)
  - SPN affiliate members (scraped from SourceWatch)

Output: atlas_spn_network.csv

Dependencies:
    pip install requests beautifulsoup4 lxml pandas openpyxl
"""

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Dict, Optional, List

import requests
from bs4 import BeautifulSoup
import pandas as pd


# ---------------------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------------------

# DeSmog Atlas global directory (derived from Wayback-scraped atlasnetwork.org)
# See: https://www.desmog.com/wp-content/uploads/2023/12/Atlas-Network-Directory-2021-Published.xlsx
ATLAS_XLSX_URL = (
    "https://www.desmog.com/wp-content/uploads/2023/12/"
    "Atlas-Network-Directory-2021-Published.xlsx"
)

# SourceWatch SPN members page (affiliates + associates + former members)
SPN_SOURCEWATCH_URL = "https://www.sourcewatch.org/index.php/SPN_Members"

# Output CSV
OUTPUT_CSV = "atlas_spn_network.csv"


# ---------------------------------------------------------------------
# UTILS
# ---------------------------------------------------------------------

def _http_get(
    url: str,
    session: Optional[requests.Session] = None,
    raise_for_status: bool = True,
    **kwargs,
) -> requests.Response:
    """
    Simple wrapper with a user-agent and basic error handling.
    """
    headers = kwargs.pop("headers", {})
    headers.setdefault(
        "User-Agent",
        "Mozilla/5.0 (compatible; atlas-spn-scraper/0.1; +https://example.org/)"
    )
    if "sourcewatch.org" in url:
        headers.setdefault(
            "Accept",
            "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        )
        headers.setdefault("Accept-Language", "en-US,en;q=0.9")
        headers.setdefault("Referer", "https://www.sourcewatch.org/")
        headers.setdefault("Cache-Control", "no-cache")
        headers.setdefault("Pragma", "no-cache")
    client = session or requests
    resp = client.get(url, headers=headers, timeout=30, **kwargs)
    if raise_for_status:
        resp.raise_for_status()
    return resp


def _find_first_column(df: pd.DataFrame, candidates: List[str]) -> Optional[str]:
    """
    Heuristic: find first column whose name contains any candidate substring.
    Case-insensitive; returns the column name or None.
    """
    lowered = {c.lower(): c for c in df.columns}
    for cand in candidates:
        cand = cand.lower()
        for lc_name, orig_name in lowered.items():
            if cand in lc_name:
                return orig_name
    return None


def _read_local_html(path_str: str) -> Optional[str]:
    path = Path(path_str)
    if not path.is_file():
        return None
    return path.read_text(encoding="utf-8")


# ---------------------------------------------------------------------
# SPN AFFILIATES FROM SOURCEWATCH
# ---------------------------------------------------------------------

def scrape_spn_affiliates(url: str = SPN_SOURCEWATCH_URL, html_path: Optional[str] = None) -> pd.DataFrame:
    """
    Scrape the 'Affiliate Members' section from SourceWatch's SPN_Members page.

    Structure (as of June 2024):
      State
      <a>Org Name</a>
      <a>Website</a>
      Phone

    We parse that pattern for each state block until we hit the next section heading.
    """
    print(f"[SPN] Fetching SourceWatch affiliates from {url}")

    local_override = html_path or os.environ.get("SPN_SOURCEWATCH_HTML")
    if local_override:
        html = _read_local_html(local_override)
        if html is None:
            raise RuntimeError(f"Local HTML not found: {local_override}")
        url = local_override
    elif Path(url).is_file():
        html = _read_local_html(url)
        if html is None:
            raise RuntimeError(f"Local HTML not found: {url}")
    else:
        session = requests.Session()
        # Warm up the session to pick up any cookies SourceWatch expects.
        try:
            _http_get("https://www.sourcewatch.org/", session=session, raise_for_status=False)
        except requests.exceptions.RequestException:
            pass

        def _try_html(fetch_url: str) -> Optional[str]:
            resp = _http_get(fetch_url, session=session, raise_for_status=False)
            if resp.status_code == 200:
                return resp.text
            print(f"[SPN] SourceWatch returned {resp.status_code} for {fetch_url}")
            return None

        html = _try_html(url)
        if html is None:
            for alt_url in (
                "https://www.sourcewatch.org/index.php?title=SPN_Members&action=render",
                "https://www.sourcewatch.org/index.php?title=SPN_Members&printable=yes",
            ):
                print(f"[SPN] Trying {alt_url}")
                html = _try_html(alt_url)
                if html:
                    url = alt_url
                    break

        if html is None:
            api_url = (
                "https://www.sourcewatch.org/api.php?action=parse"
                "&page=SPN_Members&prop=text&format=json"
            )
            resp = _http_get(api_url, session=session, raise_for_status=False)
            if resp.status_code == 200:
                data = resp.json()
                html = data.get("parse", {}).get("text", {}).get("*")
                if not html:
                    raise RuntimeError("SourceWatch API response missing parse text")
                url = api_url
            else:
                print(f"[SPN] SourceWatch returned {resp.status_code} for {api_url}")

        if html is None:
            raise RuntimeError(
                "SourceWatch blocked all automated requests (likely a human check). "
                "Open the page in your browser, pass the check, save the HTML, and "
                "rerun with --spn-html or SPN_SOURCEWATCH_HTML."
            )

    soup = BeautifulSoup(html, "lxml")


# ---------------------------------------------------------------------
# ATLAS PARTNERS FROM DESMOG DIRECTORY XLSX
# ---------------------------------------------------------------------

def load_atlas_partners_from_desmog(xlsx_url: str = ATLAS_XLSX_URL) -> pd.DataFrame:
    """
    Load the Atlas Network partner list from the DeSmog Excel, which is itself
    a scrape of the Atlas Network Global Directory via Wayback.

    The spreadsheet structure may change; this function uses heuristics to find:
      - organization name
      - country
      - city (if present)
      - region
      - a 'Resource URL' field (often a Wayback or atlas-legacy link)

    If the column names don't match the heuristics, the script will print the
    columns it found so you can adjust the mapping.
    """
    print(f"[Atlas] Downloading Atlas directory from {xlsx_url}")
    resp = _http_get(xlsx_url)
    # Save to an in-memory buffer for pandas
    from io import BytesIO
    buf = BytesIO(resp.content)

    # Some Excel files have multiple sheets; pick the one with 'Resource URL'
    print("[Atlas] Reading Excel workbook...")
    xls = pd.read_excel(buf, sheet_name=None)

    atlas_df_raw = None
    chosen_sheet = None
    for sheet_name, df in xls.items():
        if any("resource url" in str(c).lower() for c in df.columns):
            atlas_df_raw = df
            chosen_sheet = sheet_name
            break

    if atlas_df_raw is None:
        print("[Atlas] Could not find a sheet with a 'Resource URL' column.")
        print("[Atlas] Available sheets and columns were:")
        for sheet_name, df in xls.items():
            print(f"  - {sheet_name}: {list(df.columns)}")
        raise RuntimeError("Please inspect the Excel file and update column mappings manually.")

    print(f"[Atlas] Using sheet: {chosen_sheet}")
    print("[Atlas] Columns:", list(atlas_df_raw.columns))

    # Heuristically locate columns
    col_name = _find_first_column(atlas_df_raw, ["Organization", "Partner", "Name"])
    col_country = _find_first_column(atlas_df_raw, ["Country"])
    col_city = _find_first_column(atlas_df_raw, ["City"])
    col_region = _find_first_column(atlas_df_raw, ["Region"])
    col_resource = _find_first_column(atlas_df_raw, ["Resource URL", "Resource", "URL"])

    if not col_name:
        raise RuntimeError("Could not identify an organization name column in Atlas directory.")
    if not col_resource:
        raise RuntimeError("Could not identify a 'Resource URL' column in Atlas directory.")

    print("[Atlas] Detected columns:")
    print("  org_name:", col_name)
    print("  country :", col_country)
    print("  city    :", col_city)
    print("  region  :", col_region)
    print("  resource:", col_resource)

    # Build a normalized dataframe
    selected_cols = [col_name, col_resource]
    if col_country:
        selected_cols.append(col_country)
    if col_city:
        selected_cols.append(col_city)
    if col_region:
        selected_cols.append(col_region)

    df = atlas_df_raw[selected_cols].copy()

    rename_map: Dict[str, str] = {
        col_name: "child_org",
        col_resource: "atlas_resource_url",
    }
    if col_country:
        rename_map[col_country] = "child_country"
    if col_city:
        rename_map[col_city] = "child_city"
    if col_region:
        rename_map[col_region] = "atlas_region"

    df = df.rename(columns=rename_map)

    # Tag with parent metadata
    df["parent_network"] = "Atlas"
    df["parent_org"] = "Atlas Network"
    df["relationship_type"] = "partner"

    # Basic cleaning
    df = df[df["child_org"].notna()].copy()
    df["child_org"] = df["child_org"].astype(str).str.strip()

    # Reorder columns for consistency
    cols_order = [
        "parent_network",
        "parent_org",
        "relationship_type",
        "child_org",
        "child_city" if "child_city" in df.columns else None,
        "child_country" if "child_country" in df.columns else None,
        "atlas_region" if "atlas_region" in df.columns else None,
        "atlas_resource_url",
    ]
    cols_order = [c for c in cols_order if c is not None]
    df = df[cols_order]

    print(f"[Atlas] Parsed {len(df)} partners from DeSmog directory")
    return df


# ---------------------------------------------------------------------
# MAIN: COMBINE AND SAVE
# ---------------------------------------------------------------------

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a combined Atlas Network + SPN affiliates dataset"
    )
    parser.add_argument(
        "--spn-url",
        default=SPN_SOURCEWATCH_URL,
        help="SourceWatch SPN members URL (ignored when --spn-html is used)",
    )
    parser.add_argument(
        "--spn-html",
        help="Path to a saved SPN_Members HTML file",
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    # Atlas partners (global)
    atlas_df = load_atlas_partners_from_desmog(ATLAS_XLSX_URL)

    # SPN affiliates (US states)
    spn_df = scrape_spn_affiliates(args.spn_url, html_path=args.spn_html)

    # Make sure SPN has a compatible set of columns
    # We'll align on a superset of columns for the combined dataset.
    # For missing fields, fill with NaN.
    common_cols = [
        "parent_network",
        "parent_org",
        "relationship_type",
        "child_org",
        "child_city",
        "child_state_province",
        "child_country",
        "atlas_region",
        "atlas_resource_url",
        "child_website",
        "child_phone",
        "source_page",
    ]

    # Normalize Atlas DF to these columns
    for col in common_cols:
        if col not in atlas_df.columns:
            atlas_df[col] = pd.NA
    atlas_df["child_state_province"] = pd.NA
    atlas_df["child_website"] = pd.NA
    atlas_df["child_phone"] = pd.NA
    atlas_df["source_page"] = ATLAS_XLSX_URL

    atlas_df = atlas_df[common_cols]

    # Normalize SPN DF
    for col in common_cols:
        if col not in spn_df.columns:
            spn_df[col] = pd.NA
    # SPN has state, but not city or atlas_region/resource
    spn_df["child_city"] = pd.NA
    spn_df["atlas_region"] = pd.NA
    spn_df["atlas_resource_url"] = pd.NA

    spn_df = spn_df[common_cols]

    combined = pd.concat([atlas_df, spn_df], ignore_index=True)

    print(f"[MAIN] Combined dataset size: {len(combined)} rows")
    combined.to_csv(OUTPUT_CSV, index=False)
    print(f"[MAIN] Wrote {OUTPUT_CSV}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
