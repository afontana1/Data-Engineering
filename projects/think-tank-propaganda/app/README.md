# README

## Pipeline overview

All data processing lives in the `etl` folder. Run the scripts from that directory.

```
cd etl
```

Run the scripts in this order to produce the final dataset.

1) Start from raw inputs
- `Atlas-Network-Directory-2021-Published.xlsx` (Atlas directory export)
- `SPN Members - SourceWatch.html` (saved SourceWatch page)

2) Parse SPN members from HTML (writes two CSVs)
```
python parse_spn.py "SPN Members - SourceWatch.html"
```
Outputs: `spn_affiliate_members.csv`, `spn_associate_members.csv`

3) Combine Atlas + SPN affiliate members into a single master CSV
```
python combine_master.py --atlas "Atlas-Network-Directory-2021-Published.xlsx" --spn spn_affiliate_members.csv --out atlas_spn_master.csv
```
Output: `atlas_spn_master.csv`

4) Enrich missing `location` values
```
python enrich_locations.py --in atlas_spn_master.csv --out atlas_spn_master_enriched.csv
```
Output: `atlas_spn_master_enriched.csv`

5) Add `lat`/`lon` and infer missing `region`
```
python enrich_locations_lat_lon.py --in atlas_spn_master_enriched.csv --out atlas_snp_master_enriched_location.csv
```
Output: `atlas_snp_master_enriched_location.csv`

6) Standardize region labels (writes `final.csv`)
```
python standardize_regions.py --in atlas_snp_master_enriched_location.csv
```
Output: `final.csv`

7) Deduplicate and convert to JSON (writes `final.json`)
```
python csv_to_json.py
```
Output: `final.json`

## Notes

- Set your OpenAI key in the environment to avoid using the hardcoded fallback:
```
$env:OPENAI_API_KEY = "your-key-here"
```
- You can adjust output paths with each script’s `--out` flag if needed.
