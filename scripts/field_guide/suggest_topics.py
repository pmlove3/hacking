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


def _import_sklearn():
    try:
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.decomposition import NMF
    except ImportError:
        sys.exit(
            "scikit-learn is required for topic modeling.\n"
            "Install it with: pip install scikit-learn"
        )
    return TfidfVectorizer, NMF


def vectorize_and_fit(documents, n_topics, max_df=0.90, min_df=2, ngram_range=(1, 2)):
    """Fit TF-IDF + NMF over the given documents. Deterministic (init='nndsvd',
    random_state=42), per research: NMF-over-TF-IDF is the better fit for
    short documents, LDA needs much larger corpora to be stable."""
    TfidfVectorizer, NMF = _import_sklearn()
    vectorizer = TfidfVectorizer(
        max_df=max_df, min_df=min_df, stop_words="english", ngram_range=ngram_range
    )
    matrix = vectorizer.fit_transform(documents)
    nmf_model = NMF(n_components=n_topics, init="nndsvd", random_state=42, max_iter=500)
    doc_topic_matrix = nmf_model.fit_transform(matrix)
    return vectorizer, nmf_model, doc_topic_matrix


def top_terms_per_topic(vectorizer, nmf_model, top_n: int) -> list:
    feature_names = vectorizer.get_feature_names_out()
    topics = []
    for component in nmf_model.components_:
        top_indices = component.argsort()[::-1][:top_n]
        topics.append([feature_names[i] for i in top_indices])
    return topics


def top_examples_per_topic(doc_topic_matrix, items: list, top_n: int) -> list:
    examples = []
    for topic_idx in range(doc_topic_matrix.shape[1]):
        scores = doc_topic_matrix[:, topic_idx]
        top_doc_indices = scores.argsort()[::-1][:top_n]
        examples.append([items[i].get("title", "") for i in top_doc_indices])
    return examples


def format_report(topics_terms: list[list[str]], topics_examples: list[list[str]]) -> str:
    """Render topics' top terms and example item titles as a Markdown report."""
    lines = []
    for i, (terms, examples) in enumerate(zip(topics_terms, topics_examples), start=1):
        lines.append(f"## Topic {i}")
        lines.append("")
        lines.append("**Top terms:** " + ", ".join(terms))
        lines.append("")
        lines.append("**Example items:**")
        for title in examples:
            lines.append(f"- {title}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--input", required=True, help="Path to excerpts.json from step 1")
    ap.add_argument("--topics", type=int, default=12, help="Number of topics to discover")
    ap.add_argument("--top-words", type=int, default=12, help="Top terms to show per topic")
    ap.add_argument("--examples", type=int, default=5, help="Example item titles to show per topic")
    ap.add_argument("--output", help="Write the report to this file instead of printing it")
    args = ap.parse_args()

    items = json.loads(Path(args.input).read_text())
    documents = build_documents(items)

    vectorizer, nmf_model, doc_topic_matrix = vectorize_and_fit(documents, n_topics=args.topics)
    topics_terms = top_terms_per_topic(vectorizer, nmf_model, args.top_words)
    topics_examples = top_examples_per_topic(doc_topic_matrix, items, args.examples)
    report = format_report(topics_terms, topics_examples)

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report)
        print(f"Wrote topic report to {out_path}")
    else:
        print(report)


if __name__ == "__main__":
    main()
