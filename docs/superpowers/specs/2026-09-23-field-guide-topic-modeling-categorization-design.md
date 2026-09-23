# Field guide categorization: whole-word matching + local topic-modeling assist

## Purpose
Improve the categorization step of the [field guide workflow](../../zotero_to_wiki_field_guide_workflow.md) (`scripts/field_guide/categorize.py`) in two ways:

1. Fix a correctness bug: keyword matching currently uses substring containment, which produces false positives.
2. Give the person writing a new source's `categories.json` a data-driven starting point instead of guesswork, via a new local (offline) topic-modeling script.

## Background
The categorization step sorts each source's flattened items (`work/excerpts.json`) into thematic buckets by matching keywords (from a per-source `categories.json`) against each item's title + tags. In initial testing against the real lifehacker export, a plausible-looking `categories.json` sent 226 of 319 items (71%) into the `Miscellaneous` catch-all — partly because keyword lists are hand-guessed with no visibility into what's actually in the corpus, and partly because substring matching is imprecise (e.g. keyword `"art"` matches `"apartment"`, `"smart"`).

Both changes are scoped tightly: no change to the deterministic nature of `categorize.py` itself, no LLM/API calls introduced, and no change to any other pipeline step (`extract_excerpts.py`, `chunk.py`, `merge_and_fix_footnotes.py`, `validate.py`).

## Research notes
- **NMF-over-TF-IDF vs LDA-over-counts for short documents** (~100-150 words each, a few hundred docs per source): NMF-over-TF-IDF is the established better fit. LDA is a generative model over raw word-count co-occurrence and needs much larger corpora (roughly 1,000+ docs) to fit stable topics; short documents starve it of signal. NMF's non-negative factorization on TF-IDF-weighted input produces more distinct, separable topics on short text. Source: [scikit-learn's own NMF/LDA example](https://scikit-learn.org/stable/auto_examples/applications/plot_topics_extraction_with_nmf_lda.html) uses exactly this pairing; corroborated by [ScienceDirect short-text LDA-vs-NMF study](https://www.sciencedirect.com/science/article/abs/pii/S0950705118304076) and a [Towards Data Science comparison](https://towardsdatascience.com/topic-modeling-with-lsa-plsa-lda-nmf-bertopic-top2vec-a-comparison-5e6ce4b1e4a5/).
- **Reasonable defaults**: `TfidfVectorizer(max_df=0.90, min_df=2, stop_words='english', ngram_range=(1,2))` (sklearn's canonical example uses these `max_df`/`min_df` values; `ngram_range=(1,2)` catches short noun-phrases common in headlines/titles). `NMF(init='nndsvd')` for deterministic, reproducible topics (vs random init, which is unstable across re-runs). scikit-learn has no built-in heuristic for choosing `n_components` (number of topics) — common practice for a few hundred short docs is 5-15, refined by inspection.
- **Pitfalls to guard against**: sparsity can produce single-term-dominated or unstable topics (mitigated by `min_df=2` and `init='nndsvd'`); too-low `min_df` lets rare/misspelled tokens hijack a topic; too-high `max_df` erases genuinely topical repeated terms.
- Sources: see links above, plus [PMC short-text topic modeling evaluation](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11127968/).

## Design

### 1. Fix `categorize.py` keyword matching
Replace the current substring check:
```python
if any(kw.lower() in haystack for kw in keywords):
```
with whole-word/whole-phrase regex matching:
```python
if any(re.search(rf"\b{re.escape(kw.lower())}\b", haystack) for kw in keywords):
```
This eliminates false positives like `"art"` matching `"apartment"` while still correctly matching multi-word keywords like `"credit card"` (the `\b` anchors span the full phrase).

**Trade-off, documented rather than silently absorbed:** whole-word matching removes the incidental stemming substring matching provided — `"invest"` will no longer match `"investing"`/`"investment"`. The `categorize.py` docstring and `sources/lifehacker/categories.json` will be updated to state that keyword lists should list the inflected forms you actually want to catch.

### 2. New script: `scripts/field_guide/suggest_topics.py`
A read-only reporting tool — it never writes `categories.json` itself. Purpose: let the person building a new source's `categories.json` see what's actually in the corpus before guessing keywords.

**Pipeline:**
1. Load `excerpts.json`, build one document per item as `title + " " + excerpt`.
2. `TfidfVectorizer(max_df=0.90, min_df=2, stop_words='english', ngram_range=(1,2))` to vectorize.
3. `NMF(n_components=N, init='nndsvd', random_state=42)` to factorize (deterministic across runs).
4. For each topic, print:
   - Top `--top-words` (default 12) terms by weight in that topic's component.
   - Top `--examples` (default 5) item titles by that topic's weight in the document-topic matrix, so the person can eyeball real examples, not just abstract terms.

**CLI:**
```
python3 scripts/field_guide/suggest_topics.py \
  --input sources/<name>/work/excerpts.json \
  --topics 12 \
  --top-words 12 \
  --examples 5 \
  [--output sources/<name>/work/topic_report.md]
```
Without `--output`, the report prints to stdout; with it, the report is written as Markdown (one `## Topic N` section per topic, a bullet list of top terms, and a bullet list of example titles) so it can be kept alongside other `work/` artifacts for reference.

**New dependency:** `scikit-learn` (pulls in `scipy`; `numpy` is already available). Documented in the workflow doc's Prerequisites section alongside the existing PyMuPDF requirement.

### Error handling
- If `scikit-learn` is not installed, exit with a clear message (`pip install scikit-learn`), matching the existing pattern in `extract_excerpts.py` for a missing PyMuPDF.
- If the corpus is smaller than `--topics` × a small margin (too few documents for the requested topic count), let `NMF` raise naturally rather than adding custom validation — this is a rare, self-explanatory failure (`n_components` can't exceed `n_samples`/vocabulary size) not worth extra code.

### Testing
- Run `suggest_topics.py` against the real `sources/lifehacker/work/excerpts.json` (319 items) with default settings and confirm it produces coherent, human-readable topics (spot check) and doesn't crash.
- Run the updated `categorize.py` against the same data with a `categories.json` containing a deliberately substring-prone keyword (e.g. `"art"`) and confirm it no longer over-matches, while confirmed multi-word keywords still match.
- No changes to `validate.py` or other scripts — no regression testing needed there beyond confirming the pipeline as a whole still runs end-to-end for lifehacker (already covered in the initial build; this change doesn't touch those scripts).

## Out of scope
- No LLM/API calls anywhere in this change.
- No automatic classification — `categories.json` remains hand-maintained.
- No change to `chunk.py`, `extract_excerpts.py`, `merge_and_fix_footnotes.py`, `validate.py`, or the documented step order.
- No stemming/lemmatization added to `categorize.py` — the fix is precision-only (whole-word matching); recall is the keyword list author's responsibility, informed by the new topic report.
