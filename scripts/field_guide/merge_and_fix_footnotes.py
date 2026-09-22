#!/usr/bin/env python3
"""
Step 5 of the field-guide workflow: concatenate independently-synthesized
section Markdown files and renumber their footnotes into one global,
sequential sequence, ending with a single "### References" block.

Each input section file is expected to contain its own heading(s), body
paragraphs with inline citations like [^1], and footnote definitions like:

    [^1]: [Article Title](https://example.com/article)

at the bottom. Sections are concatenated in the order given, footnotes are
renumbered in the order sections are provided (and in order of first
appearance within each section), and a single References block is appended.

Usage (explicit order):
    python3 merge_and_fix_footnotes.py \
        --output sources/<name>/work/merged_draft.md \
        sources/<name>/work/sections/section_finance.md \
        sources/<name>/work/sections/section_health.md \
        ...

Usage (alphabetical order from a directory):
    python3 merge_and_fix_footnotes.py \
        --sections-dir sources/<name>/work/sections \
        --output sources/<name>/work/merged_draft.md
"""
import argparse
import re
from pathlib import Path

DEF_RE = re.compile(r"^\[\^(\d+)\]:\s*(.*)$")
REF_RE = re.compile(r"\[\^(\d+)\](?!:)")


def split_body_and_defs(text: str):
    body_lines = []
    defs = {}
    for line in text.splitlines():
        m = DEF_RE.match(line.strip())
        if m:
            defs[m.group(1)] = m.group(2)
        else:
            body_lines.append(line)
    body = "\n".join(body_lines).rstrip() + "\n"
    return body, defs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("sections", nargs="*", help="Section markdown files, in the desired final order")
    ap.add_argument("--sections-dir", help="Directory of *.md section files, used in sorted-name order if 'sections' is omitted")
    ap.add_argument("--output", required=True, help="Path to write the merged, renumbered draft")
    ap.add_argument("--intro", help="Optional path to a markdown file to prepend before all sections (e.g. title + editorial note)")
    args = ap.parse_args()

    if args.sections:
        files = [Path(p) for p in args.sections]
    elif args.sections_dir:
        files = sorted(Path(args.sections_dir).glob("*.md"))
    else:
        raise SystemExit("Provide section files as positional args or --sections-dir")

    global_defs = []  # list of (global_id, definition_text)
    next_id = 1
    merged_bodies = []

    for f in files:
        text = f.read_text()
        body, defs = split_body_and_defs(text)

        # Map local -> global id, sorted by local id for stable ordering.
        local_ids = sorted(defs.keys(), key=int)
        local_to_global = {}
        for local_id in local_ids:
            local_to_global[local_id] = next_id
            global_defs.append((next_id, defs[local_id]))
            next_id += 1

        # Two-pass substitution via placeholders to avoid id collisions
        # between this file's local numbers and already-assigned globals.
        def to_placeholder(m):
            local_id = m.group(1)
            if local_id in local_to_global:
                return f"@@FN{local_to_global[local_id]}@@"
            return m.group(0)  # leave untouched if no matching definition

        body = REF_RE.sub(to_placeholder, body)
        body = re.sub(r"@@FN(\d+)@@", r"[^\1]", body)

        merged_bodies.append(body.strip("\n"))

        first_global = local_to_global.get(local_ids[0]) if local_ids else "-"
        last_global = next_id - 1 if local_ids else "-"
        print(f"{f.name}: {len(defs)} definition(s) merged (global {first_global}-{last_global})")

    out_parts = []
    if args.intro:
        out_parts.append(Path(args.intro).read_text().rstrip())
    out_parts.append("\n\n".join(merged_bodies))
    out_parts.append("### References\n\n" + "\n".join(f"[^{gid}]: {text}" for gid, text in global_defs))

    Path(args.output).write_text("\n\n".join(out_parts) + "\n")
    print(f"\nWrote {len(global_defs)} total footnotes to {args.output}")


if __name__ == "__main__":
    main()
