#!/usr/bin/env python3
"""
Step 3 of the field-guide workflow: split each category JSON file into
small chunks so an LLM can synthesize every item without silently dropping
any (LLMs tend to omit items from long lists).

Usage:
    python3 chunk.py \
        --indir sources/<name>/work/categories \
        --outdir sources/<name>/work/chunks \
        --size 20
"""
import argparse
import json
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--indir", required=True, help="Directory of per-category JSON files from step 2")
    ap.add_argument("--outdir", required=True, help="Directory to write chunked JSON files")
    ap.add_argument("--size", type=int, default=20, help="Max items per chunk (15-20 recommended)")
    args = ap.parse_args()

    indir = Path(args.indir)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    total_chunks = 0
    for cat_file in sorted(indir.glob("*.json")):
        items = json.loads(cat_file.read_text())
        name = cat_file.stem
        num_chunks = (len(items) + args.size - 1) // args.size or 1
        for i in range(num_chunks):
            part = items[i * args.size:(i + 1) * args.size]
            if not part:
                continue
            out_path = outdir / f"{name}_part{i + 1}.json"
            out_path.write_text(json.dumps(part, indent=2, ensure_ascii=False))
            total_chunks += 1
        print(f"{name}: {len(items)} item(s) -> {num_chunks} chunk(s)")

    print(f"Wrote {total_chunks} chunk file(s) to {outdir}")


if __name__ == "__main__":
    main()
