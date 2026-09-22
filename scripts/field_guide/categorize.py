#!/usr/bin/env python3
"""
Step 2 of the field-guide workflow: sort flattened excerpt items into
thematic categories by keyword matching against title + tags.

Usage:
    python3 categorize.py \
        --input sources/<name>/work/excerpts.json \
        --config sources/<name>/categories.json \
        --outdir sources/<name>/work/categories

The category config is a JSON object mapping category name -> list of
lowercase keywords, e.g.:

    {
      "Finance_Money": ["money", "tax", "budget", "credit", "loan"],
      "Health_Diet_Fitness": ["health", "diet", "fitness", "sleep", "workout"]
    }

Items are assigned to the FIRST category whose keyword matches (checked in
config order), so put more specific categories earlier. Items matching no
category go to a catch-all bucket (default name: "Miscellaneous").
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="Path to excerpts.json from step 1")
    ap.add_argument("--config", required=True, help="Path to categories.json keyword config")
    ap.add_argument("--outdir", required=True, help="Directory to write one JSON file per category")
    ap.add_argument("--catchall", default="Miscellaneous", help="Category name for unmatched items")
    args = ap.parse_args()

    items = json.loads(Path(args.input).read_text())
    categories = json.loads(Path(args.config).read_text())

    buckets = {name: [] for name in categories}
    buckets[args.catchall] = []

    for item in items:
        haystack = " ".join([item.get("title", ""), *item.get("tags", [])]).lower()
        assigned = False
        for name, keywords in categories.items():
            if any(kw.lower() in haystack for kw in keywords):
                buckets[name].append(item)
                assigned = True
                break
        if not assigned:
            buckets[args.catchall].append(item)

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    for name, bucket_items in buckets.items():
        if not bucket_items:
            continue
        out_path = outdir / f"{name}.json"
        out_path.write_text(json.dumps(bucket_items, indent=2, ensure_ascii=False))
        print(f"{name}: {len(bucket_items)} item(s) -> {out_path}")

    total = sum(len(v) for v in buckets.values())
    print(f"Total categorized: {total} (of {len(items)} input items)")


if __name__ == "__main__":
    main()
