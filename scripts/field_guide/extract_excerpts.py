#!/usr/bin/env python3
"""
Step 1 of the field-guide workflow: flatten a Zotero Better BibTeX (BBT) JSON
export into a lightweight excerpts file.

For each top-level item (skipping standalone attachment/note entries), pulls
title/url/date/tags/creators and, if a PDF attachment is present, extracts the
first N characters of its text as a short excerpt. This keeps later LLM steps
from having to ingest full PDFs.

Usage:
    python3 extract_excerpts.py \
        --input sources/<name>/raw/<export>.json \
        --output sources/<name>/work/excerpts.json \
        --pdf-chars 800

The PDF path in the export is relative to the export JSON's own directory
(this is how Zotero writes BBT exports with attachments), so --input's
parent directory is used as the base for resolving attachment paths.
"""
import argparse
import json
import sys
from pathlib import Path


def extract_pdf_excerpt(pdf_path: Path, max_chars: int) -> str | None:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        sys.exit(
            "PyMuPDF is required for PDF excerpt extraction.\n"
            "Install it with: pip install pymupdf"
        )
    if not pdf_path.exists():
        return None
    try:
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
                if len(text) >= max_chars:
                    break
    except Exception as exc:
        print(f"  warning: could not read {pdf_path.name}: {exc}", file=sys.stderr)
        return None
    text = " ".join(text.split())
    return text[:max_chars] or None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="Path to the Zotero BBT JSON export")
    ap.add_argument("--output", required=True, help="Path to write the flattened excerpts JSON")
    ap.add_argument("--pdf-chars", type=int, default=800, help="Max characters of PDF text to keep per item")
    args = ap.parse_args()

    in_path = Path(args.input)
    base_dir = in_path.parent
    data = json.loads(in_path.read_text())
    items = data.get("items", data if isinstance(data, list) else [])

    results = []
    skipped_no_key = 0
    for item in items:
        if item.get("itemType") in ("attachment", "note"):
            continue

        key = item.get("citationKey") or item.get("itemKey")
        if not key:
            skipped_no_key += 1
            continue

        excerpt = None
        for att in item.get("attachments", []):
            path = att.get("path")
            if path and path.lower().endswith(".pdf"):
                excerpt = extract_pdf_excerpt(base_dir / path, args.pdf_chars)
                if excerpt:
                    break

        results.append({
            "key": key,
            "title": item.get("title", ""),
            "url": item.get("url", ""),
            "date": item.get("date", ""),
            "tags": [t.get("tag", "") for t in item.get("tags", [])],
            "creators": [
                f"{c.get('firstName', '')} {c.get('lastName', '')}".strip()
                for c in item.get("creators", [])
            ],
            "excerpt": excerpt or item.get("abstractNote", ""),
        })

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(results, indent=2, ensure_ascii=False))

    print(f"Wrote {len(results)} items to {out_path}")
    if skipped_no_key:
        print(f"Skipped {skipped_no_key} item(s) with no citation key")


if __name__ == "__main__":
    main()
