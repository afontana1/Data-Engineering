#!/usr/bin/env python3
"""
Combine Atlas Network (Data tab) with SPN affiliate members into a master dataset.

Dependencies:
  pip install pandas openpyxl
"""

import argparse
from typing import List

import pandas as pd


DEFAULT_ATLAS_PATH = "Atlas-Network-Directory-2021-Published.xlsx"
DEFAULT_SPN_PATH = "spn_affiliate_members.csv"
DEFAULT_OUT_PATH = "atlas_spn_master.csv"


def _ensure_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    for col in columns:
        if col not in df.columns:
            df[col] = pd.NA
    return df


def load_atlas(path: str) -> pd.DataFrame:
    df = pd.read_excel(path, sheet_name="Data")

    rename_map = {
        "Org name": "org_name",
        "Org Name Overarching": "org_name_overarching",
        "Org_link": "sourcewatch_page_url",
        "Website_link": "website",
        "State/Province": "state_province",
        "Country Code": "country",
    }
    df = df.rename(columns=rename_map)

    df["institution"] = "atlas"

    keep_cols = [
        "institution",
        "org_name",
        "Region",
        "Location",
        "City",
        "state_province",
        "country",
        "website",
        "sourcewatch_page_url",
    ]

    df = _ensure_columns(df, keep_cols)
    return df[keep_cols]


def load_spn(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)

    rename_map = {
        "org_name": "org_name",
        "website": "website",
        "state": "state_province",
        "sourcewatch_page_url": "sourcewatch_page_url",
    }

    df = df.rename(columns=rename_map)
    df["institution"] = "spn"

    keep_cols = [
        "institution",
        "org_name",
        "region",
        "location",
        "city",
        "state_province",
        "country",
        "website",
        "sourcewatch_page_url",
    ]

    df = _ensure_columns(df, keep_cols)
    return df[keep_cols]


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Combine Atlas Network Data with SPN affiliate members",
    )
    parser.add_argument(
        "--atlas",
        default=DEFAULT_ATLAS_PATH,
        help="Path to Atlas Network directory XLSX",
    )
    parser.add_argument(
        "--spn",
        default=DEFAULT_SPN_PATH,
        help="Path to SPN affiliate members CSV",
    )
    parser.add_argument(
        "--out",
        default=DEFAULT_OUT_PATH,
        help="Output CSV path",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()

    atlas = load_atlas(args.atlas)
    spn = load_spn(args.spn)

    # Normalize Atlas columns to match SPN naming
    atlas = atlas.rename(
        columns={
            "Region": "region",
            "Location": "location",
            "City": "city",
        }
    )

    common_cols = [
        "institution",
        "org_name",
        "region",
        "location",
        "city",
        "state_province",
        "country",
        "website",
        "sourcewatch_page_url",
    ]

    atlas = _ensure_columns(atlas, common_cols)
    spn = _ensure_columns(spn, common_cols)

    combined = pd.concat([atlas[common_cols], spn[common_cols]], ignore_index=True)
    combined.to_csv(args.out, index=False)
    print(f"[MASTER] Atlas rows: {len(atlas)}")
    print(f"[MASTER] SPN rows: {len(spn)}")
    print(f"[MASTER] Combined rows: {len(combined)} -> {args.out}")


if __name__ == "__main__":
    main()
