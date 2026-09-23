#!/usr/bin/env python3
"""
Assist tool for the field-guide workflow: local (offline) topic modeling
over a source's excerpts, to help a person write a better categories.json
before running categorize.py.

This is a READ-ONLY report generator — it never writes categories.json
itself. It prints (or saves) each discovered topic's top terms plus a few
example item titles, so you can see what's actually in the corpus.

Usage:
    python3 suggest_topics.py \
        --input sources/<name>/work/excerpts.json \
        --topics 12 \
        --top-words 12 \
        --examples 5 \
        [--output sources/<name>/work/topic_report.md]
"""
import argparse
import json
import sys
from pathlib import Path


def build_documents(items: list[dict]) -> list[str]:
    """One document per item: title + excerpt, whichever parts are present."""
    documents = []
    for item in items:
        parts = [item.get("title", ""), item.get("excerpt", "")]
        documents.append(" ".join(p for p in parts if p).strip())
    return documents


if __name__ == "__main__":
    pass
