# Field Guide Categorization: Whole-Word Matching + Topic-Modeling Assist Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superjawn:subagent-driven-development (recommended) or superjawn:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix a false-positive bug in `categorize.py`'s keyword matching, and add a new local (offline, scikit-learn) topic-modeling script that helps a person write better `categories.json` keyword lists for any source.

**Architecture:** `categorize.py` gets a small, independently-testable `matches_category()` function using whole-word regex matching in place of substring containment. A new `scripts/field_guide/suggest_topics.py` is built from four pure, testable functions (`build_documents`, `vectorize_and_fit`, `top_terms_per_topic`, `top_examples_per_topic`, `format_report`) wired together by a thin argparse `main()`, following the same CLI-script shape as the other `scripts/field_guide/*.py` files. Neither script writes `categories.json` — `suggest_topics.py` only prints/saves a human-readable report.

**Tech Stack:** Python 3 stdlib (`re`, `argparse`, `json`, `pathlib`) for `categorize.py`; `scikit-learn` (`TfidfVectorizer`, `NMF`) for `suggest_topics.py`; `pytest` for tests (new dev dependency, not required to run the pipeline itself).

**Spec:** [docs/superpowers/specs/2026-09-23-field-guide-topic-modeling-categorization-design.md](../specs/2026-09-23-field-guide-topic-modeling-categorization-design.md)

---

## File Structure

- **Modify:** `scripts/field_guide/categorize.py` — add `matches_category()`, refactor `main()` to use it, update the module docstring.
- **Modify:** `sources/lifehacker/categories.json` — add inflected keyword forms so recall isn't lost by the whole-word-matching switch. This path is inside `sources/`, which `.gitignore` excludes — this edit is **local only**, no `git add`/commit for this file.
- **Modify:** `docs/zotero_to_wiki_field_guide_workflow.md` — add `scikit-learn` to Prerequisites, add `suggest_topics.py` usage to the Step 2 section.
- **Create:** `scripts/field_guide/suggest_topics.py` — new topic-modeling assist script.
- **Create:** `tests/conftest.py` — puts `scripts/field_guide/` on `sys.path` so tests can `import categorize` / `import suggest_topics` directly.
- **Create:** `tests/test_categorize.py`
- **Create:** `tests/test_suggest_topics.py`

Before Task 1, install test/runtime dependencies:

```bash
pip install pytest scikit-learn
```

---

### Task 1: Fix `categorize.py`'s keyword matching (whole-word, not substring)

**Files:**
- Create: `tests/conftest.py`
- Create: `tests/test_categorize.py`
- Modify: `scripts/field_guide/categorize.py`

- [ ] **Step 1: Create the pytest path setup**

Create `tests/conftest.py`:

```python
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "scripts" / "field_guide"
sys.path.insert(0, str(SCRIPTS_DIR))
```

- [ ] **Step 2: Write the failing tests**

Create `tests/test_categorize.py`:

```python
from categorize import matches_category


def test_whole_word_match_succeeds():
    assert matches_category("an article about art history", ["art"]) is True


def test_substring_false_positive_is_rejected():
    assert matches_category("looking for a new apartment", ["art"]) is False
    assert matches_category("she seemed smart today", ["art"]) is False


def test_multi_word_keyword_matches_as_phrase():
    assert matches_category("check your credit card statement", ["credit card"]) is True


def test_multi_word_keyword_does_not_match_partial_overlap():
    assert matches_category("apply for a credit union loan", ["credit card"]) is False


def test_keyword_is_lowercased_before_matching():
    assert matches_category("this covers tax season", ["Tax"]) is True
```

- [ ] **Step 3: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_categorize.py -v`
Expected: FAIL — `ImportError: cannot import name 'matches_category' from 'categorize'` (the function doesn't exist yet).

- [ ] **Step 4: Implement `matches_category()` and refactor `main()`**

In `scripts/field_guide/categorize.py`, add `import re` to the imports (line 24-26 block becomes):

```python
import argparse
import json
import re
from pathlib import Path
```

Add the new function right after the imports, before `def main():`:

```python
def matches_category(haystack: str, keywords: list[str]) -> bool:
    """Whole-word/whole-phrase match: avoids substring false positives like
    keyword "art" matching "apartment" or "smart"."""
    return any(re.search(rf"\b{re.escape(kw.lower())}\b", haystack) for kw in keywords)
```

Replace the matching line inside `main()`'s loop (currently `if any(kw.lower() in haystack for kw in keywords):`) with:

```python
        for name, keywords in categories.items():
            if matches_category(haystack, keywords):
                buckets[name].append(item)
                assigned = True
                break
```

- [ ] **Step 5: Update the module docstring**

Replace the docstring's category-config paragraph (currently ending "...so put more specific categories earlier. Items matching no category go to a catch-all bucket (default name: "Miscellaneous").") by appending this paragraph right after it, still inside the `"""..."""` docstring:

```
Keywords are matched as whole words/phrases (not substrings), so "art" will
NOT match "apartment" or "smart". This means keyword lists need to list the
inflected forms you actually want to catch, e.g. use
["invest", "investing", "investment", "investor"] instead of relying on
"invest" to substring-match "investing".
```

- [ ] **Step 6: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_categorize.py -v`
Expected: PASS (5 passed)

- [ ] **Step 7: Commit**

```bash
git add scripts/field_guide/categorize.py tests/conftest.py tests/test_categorize.py
git commit -m "fix: whole-word keyword matching in categorize.py to avoid substring false positives"
```

---

### Task 2: Verify the fix against real data and update the local lifehacker keyword list

**Files:**
- Modify (local only, not committed): `sources/lifehacker/categories.json`

- [ ] **Step 1: Re-run categorize.py against the real lifehacker excerpts**

First regenerate excerpts if not already present from earlier testing:

```bash
python3 scripts/field_guide/extract_excerpts.py \
  --input sources/lifehacker/raw/Articles_Lifehacker.json \
  --output sources/lifehacker/work/excerpts.json
```

Then run categorization with the existing config:

```bash
python3 scripts/field_guide/categorize.py \
  --input sources/lifehacker/work/excerpts.json \
  --config sources/lifehacker/categories.json \
  --outdir /tmp/categorize_check
```

Expected: command completes without error, prints a per-category count summary. Compare the `Miscellaneous_Lifehacks` count to a prior run (before this fix) to see the effect of removing false-positive matches — a small increase in the catch-all bucket is expected and correct (previously wrongly matched items no longer falsely match).

- [ ] **Step 2: Add inflected keyword forms to `sources/lifehacker/categories.json`**

Open `sources/lifehacker/categories.json` and extend the keyword lists so intentional substring matches keep working as whole words. At minimum, extend `"invest"` and any other stem-style keywords already present. For example, change:

```json
"Finance_Money": ["money", "tax", "budget", "credit", "loan", "debt", "salary", "invest", "retirement", "insurance"],
```

to:

```json
"Finance_Money": ["money", "tax", "taxes", "budget", "budgeting", "credit", "loan", "loans", "debt", "salary", "invest", "investing", "investment", "retirement", "insurance"],
```

Apply the same treatment (add plural/-ing/-ed forms actually used in real titles) to the other categories in the file, informed by what `--outdir /tmp/categorize_check`'s `Miscellaneous_Lifehacks.json` contains (spot check a few titles that should have matched but didn't).

This file is under `sources/`, which is gitignored — no commit step for it.

---

### Task 3: `build_documents()` for `suggest_topics.py`

**Files:**
- Create: `scripts/field_guide/suggest_topics.py`
- Create: `tests/test_suggest_topics.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_suggest_topics.py`:

```python
from suggest_topics import build_documents


def test_build_documents_combines_title_and_excerpt():
    items = [{"title": "Ask Your Loan Servicer", "excerpt": "Extra payments go to principal."}]
    assert build_documents(items) == ["Ask Your Loan Servicer Extra payments go to principal."]


def test_build_documents_handles_missing_excerpt():
    items = [{"title": "Just A Title"}]
    assert build_documents(items) == ["Just A Title"]


def test_build_documents_handles_missing_title():
    items = [{"excerpt": "Only an excerpt here."}]
    assert build_documents(items) == ["Only an excerpt here."]
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_suggest_topics.py -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'suggest_topics'` (file doesn't exist yet).

- [ ] **Step 3: Create `suggest_topics.py` with `build_documents()`**

Create `scripts/field_guide/suggest_topics.py`:

```python
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_suggest_topics.py -v`
Expected: PASS (3 passed)

- [ ] **Step 5: Commit**

```bash
git add scripts/field_guide/suggest_topics.py tests/test_suggest_topics.py
git commit -m "feat: add suggest_topics.py skeleton with build_documents()"
```

---

### Task 4: Topic extraction — `vectorize_and_fit()`, `top_terms_per_topic()`, `top_examples_per_topic()`

**Files:**
- Modify: `scripts/field_guide/suggest_topics.py`
- Modify: `tests/test_suggest_topics.py`

- [ ] **Step 1: Write the failing tests**

Append to `tests/test_suggest_topics.py`:

```python
from suggest_topics import vectorize_and_fit, top_terms_per_topic, top_examples_per_topic

CAT_CAR_ITEMS = [
    {"title": "Cats are great pets", "excerpt": "Cats love naps and cats purr all day long."},
    {"title": "My cat sleeps all day", "excerpt": "Cats are calm pets that purr and nap."},
    {"title": "Kittens are playful", "excerpt": "Kittens and cats are playful pets that nap."},
    {"title": "Cars need gas", "excerpt": "Cars drive fast and cars need fuel to race."},
    {"title": "My car has four wheels", "excerpt": "Cars race fast and cars need fuel too."},
    {"title": "Sports cars are loud", "excerpt": "Sports cars race fast and cars are loud."},
]


def test_vectorize_and_fit_separates_two_obvious_topics():
    documents = build_documents(CAT_CAR_ITEMS)
    vectorizer, nmf_model, doc_topic_matrix = vectorize_and_fit(documents, n_topics=2, min_df=2)
    topics = top_terms_per_topic(vectorizer, nmf_model, top_n=5)
    assert len(topics) == 2
    term_sets = [set(t) for t in topics]
    assert any({"cats", "cat"} & terms for terms in term_sets)
    assert any({"cars", "car"} & terms for terms in term_sets)


def test_top_examples_per_topic_picks_relevant_titles():
    documents = build_documents(CAT_CAR_ITEMS)
    vectorizer, nmf_model, doc_topic_matrix = vectorize_and_fit(documents, n_topics=2, min_df=2)
    examples = top_examples_per_topic(doc_topic_matrix, CAT_CAR_ITEMS, top_n=1)
    assert len(examples) == 2
    all_examples = {title for group in examples for title in group}
    assert any("cat" in t.lower() or "kitten" in t.lower() for t in all_examples)
    assert any("car" in t.lower() for t in all_examples)
```

(`build_documents` is already imported at the top of the file from Task 3.)

- [ ] **Step 2: Run tests to verify they fail**

Run: `python3 -m pytest tests/test_suggest_topics.py -v`
Expected: FAIL — `ImportError: cannot import name 'vectorize_and_fit' from 'suggest_topics'`

- [ ] **Step 3: Implement the three functions**

In `scripts/field_guide/suggest_topics.py`, replace the `if __name__ == "__main__": pass` placeholder at the bottom with real functions (keep everything above it, including `build_documents`):

```python
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


if __name__ == "__main__":
    pass
```

- [ ] **Step 4: Run tests to verify they pass**

Run: `python3 -m pytest tests/test_suggest_topics.py -v`
Expected: PASS (5 passed)

- [ ] **Step 5: Commit**

```bash
git add scripts/field_guide/suggest_topics.py tests/test_suggest_topics.py
git commit -m "feat: add NMF topic extraction to suggest_topics.py"
```

---

### Task 5: `format_report()`

**Files:**
- Modify: `scripts/field_guide/suggest_topics.py`
- Modify: `tests/test_suggest_topics.py`

- [ ] **Step 1: Write the failing test**

Append to `tests/test_suggest_topics.py`:

```python
from suggest_topics import format_report


def test_format_report_includes_terms_and_examples():
    topics_terms = [["cats", "purr", "nap"], ["cars", "race", "fast"]]
    topics_examples = [["Cats are great pets"], ["Cars need gas"]]
    report = format_report(topics_terms, topics_examples)
    assert "## Topic 1" in report
    assert "cats, purr, nap" in report
    assert "- Cats are great pets" in report
    assert "## Topic 2" in report
    assert "- Cars need gas" in report
```

- [ ] **Step 2: Run test to verify it fails**

Run: `python3 -m pytest tests/test_suggest_topics.py -v`
Expected: FAIL — `ImportError: cannot import name 'format_report' from 'suggest_topics'`

- [ ] **Step 3: Implement `format_report()`**

In `scripts/field_guide/suggest_topics.py`, add this function just above `if __name__ == "__main__":`:

```python
def format_report(topics_terms: list, topics_examples: list) -> str:
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `python3 -m pytest tests/test_suggest_topics.py -v`
Expected: PASS (6 passed)

- [ ] **Step 5: Commit**

```bash
git add scripts/field_guide/suggest_topics.py tests/test_suggest_topics.py
git commit -m "feat: add format_report() to suggest_topics.py"
```

---

### Task 6: Wire up the CLI and smoke-test against real data

**Files:**
- Modify: `scripts/field_guide/suggest_topics.py`

- [ ] **Step 1: Implement `main()`**

In `scripts/field_guide/suggest_topics.py`, replace `if __name__ == "__main__": pass` with:

```python
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
```

- [ ] **Step 2: Run the full test suite**

Run: `python3 -m pytest tests/ -v`
Expected: PASS (14 passed: 5 from test_categorize.py + 9 from test_suggest_topics.py)

- [ ] **Step 3: Smoke-test against real lifehacker data**

```bash
python3 scripts/field_guide/suggest_topics.py \
  --input sources/lifehacker/work/excerpts.json \
  --topics 12 \
  --output sources/lifehacker/work/topic_report.md
```

Expected: command completes without error, prints `Wrote topic report to sources/lifehacker/work/topic_report.md`. Open the file and confirm it has 12 `## Topic N` sections, each with a top-terms line and example titles that look thematically coherent (e.g. one topic dominated by finance-ish terms, another by tech-ish terms).

- [ ] **Step 4: Commit**

```bash
git add scripts/field_guide/suggest_topics.py
git commit -m "feat: wire up suggest_topics.py CLI"
```

---

### Task 7: Update the workflow documentation

**Files:**
- Modify: `docs/zotero_to_wiki_field_guide_workflow.md`

- [ ] **Step 1: Add scikit-learn to Prerequisites**

Find the "## Prerequisites" section (currently ending with `- Python 3 with \`PyMuPDF\` installed for PDF text extraction: \`pip install pymupdf\`.`) and add a new bullet immediately after it:

```markdown
- Python 3 with `scikit-learn` installed if you want to use the topic-modeling assist script in step 2: `pip install scikit-learn`.
```

- [ ] **Step 2: Document `suggest_topics.py` in the Step 2 section**

Find the "### 2. Thematic Categorization" section. After the paragraph ending "...re-tune the keyword lists for each new source's subject matter, and check the catch-all bucket's size afterward — if it's large, add more categories or keywords rather than letting one oversized "misc" bucket carry most of the source." add a new paragraph and code block:

```markdown
**Before writing `categories.json` for a new source**, run the topic-modeling assist script to see what's actually in the corpus instead of guessing keywords blind:

```bash
python3 scripts/field_guide/suggest_topics.py \
  --input sources/<name>/work/excerpts.json \
  --topics 12 \
  --output sources/<name>/work/topic_report.md
```

This is a read-only report (top terms + example item titles per discovered topic) — it does not write `categories.json` for you. Read the topics, then write your keyword lists informed by what's actually there. Keywords match as whole words/phrases (not substrings), so list the inflected forms you want to catch, e.g. `["invest", "investing", "investment"]` rather than relying on `"invest"` to substring-match `"investing"`.
```

- [ ] **Step 3: Commit**

```bash
git add docs/zotero_to_wiki_field_guide_workflow.md
git commit -m "docs: document suggest_topics.py and scikit-learn prerequisite"
```

---

### Task 8: Final end-to-end verification

**Files:** none (verification only)

- [ ] **Step 1: Run the full test suite one more time**

Run: `python3 -m pytest tests/ -v`
Expected: PASS (14 passed)

- [ ] **Step 2: Run the real pipeline end-to-end for lifehacker**

```bash
python3 scripts/field_guide/categorize.py \
  --input sources/lifehacker/work/excerpts.json \
  --config sources/lifehacker/categories.json \
  --outdir /tmp/categorize_final_check

python3 scripts/field_guide/validate.py sources/lifehacker/lifehacker_field_guide.md
```

Expected: `categorize.py` prints per-category counts summing to 319; `validate.py` prints "All checks passed." (this file is untouched by this plan, confirming no regression).

- [ ] **Step 3: Confirm git status is clean**

Run: `git status`
Expected: `nothing to commit, working tree clean` (aside from untracked files under `sources/`, which `.gitignore` excludes).

---

## Self-Review Notes

- **Spec coverage:** Task 1-2 cover spec section "1. Fix categorize.py keyword matching" including the trade-off documentation. Tasks 3-6 cover spec section "2. New script: suggest_topics.py" including all CLI flags, the read-only/no-auto-write constraint, and the `_import_sklearn` error-handling pattern matching `extract_excerpts.py`'s existing PyMuPDF guard. Task 7 covers the Prerequisites/doc update. Task 8 covers the spec's "Testing" section's end-to-end check. Out-of-scope items (no LLM/API, no other script changes, no stemming in categorize.py) are respected — no task touches `chunk.py`, `extract_excerpts.py`, `merge_and_fix_footnotes.py`, or adds stemming logic.
- **Placeholder scan:** no TBD/TODO; every step has complete, runnable code.
- **Type consistency:** `matches_category(haystack: str, keywords: list[str]) -> bool` used consistently in Task 1's test and implementation. `build_documents`, `vectorize_and_fit`, `top_terms_per_topic`, `top_examples_per_topic`, `format_report` signatures are introduced once each and reused with matching names/arg order across Tasks 3-6.
