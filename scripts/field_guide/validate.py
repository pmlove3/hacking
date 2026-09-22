#!/usr/bin/env python3
"""
Step 8 of the field-guide workflow: mechanical citation and structure check
for a finished (or in-progress) field guide Markdown file. Run this after
merging and again after any archiving/editing pass.

Checks:
  - Every inline [^N] citation has exactly one matching [^N]: definition.
  - Every [^N]: definition is referenced by at least one inline [^N].
  - No duplicate definitions for the same N.
  - Exactly one "### References" heading.
  - Warns about leftover chunk artifacts ("Part 1", "part1", etc.) outside
    of URLs.

Usage:
    python3 validate.py sources/<name>/<name>_field_guide.md
"""
import argparse
import re
import sys
from pathlib import Path

DEF_RE = re.compile(r"^\[\^(\d+)\]:", re.MULTILINE)
REF_RE = re.compile(r"\[\^(\d+)\](?!:)")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("file", help="Path to the field guide markdown file")
    args = ap.parse_args()

    text = Path(args.file).read_text()
    problems = []

    inline_ids = [int(m) for m in REF_RE.findall(text)]
    def_ids = [int(m) for m in DEF_RE.findall(text)]

    inline_set = set(inline_ids)
    def_set = set(def_ids)

    missing_defs = sorted(inline_set - def_set)
    if missing_defs:
        problems.append(f"Inline citations with no definition: {missing_defs}")

    unused_defs = sorted(def_set - inline_set)
    if unused_defs:
        problems.append(f"Unused footnote definitions: {unused_defs}")

    dupes = sorted({n for n in def_ids if def_ids.count(n) > 1})
    if dupes:
        problems.append(f"Duplicate footnote definitions: {dupes}")

    ref_headings = re.findall(r"^#{1,6}\s*References\s*$", text, re.MULTILINE)
    if len(ref_headings) != 1:
        problems.append(f"Expected exactly one References heading, found {len(ref_headings)}")

    leftover = re.findall(r"\b[Pp]art\s?\d+\b", text)
    if leftover:
        problems.append(f"Possible leftover chunk artifacts: {sorted(set(leftover))}")

    print(f"Inline citations: {len(inline_set)} unique ({len(inline_ids)} total)")
    print(f"Footnote definitions: {len(def_set)} unique ({len(def_ids)} total)")

    if problems:
        print("\nFAILED:")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)

    print("\nAll checks passed.")


if __name__ == "__main__":
    main()
