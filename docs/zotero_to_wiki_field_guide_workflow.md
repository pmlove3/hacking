# Zotero Export to Wiki-Style Field Guide Workflow

## Purpose
This workflow turns a Zotero collection export (hundreds of articles and attached PDFs) into a heavily annotated, synthesized, wiki-style Markdown field guide, with **100% citation coverage** of the source materials and an accuracy/currentness review so outdated advice ends up in an Archive section instead of being presented as current.

The workflow is **repeatable across sources**: each source (a Lifehacker export, a NYT Cooking export, a security-blog export, etc.) gets its own folder under `sources/`, and the same scripts in `scripts/field_guide/` process any of them. Nothing in the scripts is Lifehacker-specific — category names, keywords, and chunk sizes are all supplied as arguments/config per source.

## Directory layout

```
hacking/
  scripts/field_guide/          # reusable, source-agnostic scripts (see below)
  sources/
    <source_name>/
      raw/                      # the Zotero BBT JSON export + its files/ folder, as exported
      categories.json           # keyword config for this source (edit per source)
      work/                     # all intermediate, disposable artifacts
        excerpts.json           # step 1 output
        categories/*.json       # step 2 output, one file per category
        chunks/*.json           # step 3 output, categories split into 15-20 item chunks
        sections/*.md           # step 4 output, one hand/LLM-synthesized .md per chunk
        merged_draft.md         # step 5 output, footnotes globally renumbered
      <source_name>_field_guide.md   # FINAL published output (step 6-8 applied to merged_draft.md)
```

`sources/lifehacker/` is populated this way already and doubles as a worked example — every path below has a concrete lifehacker equivalent you can open and compare against.

Everything under a source's `work/` directory is throwaway/regeneratable from `raw/` + `categories.json`; only `raw/`, `categories.json`, and the final `<source_name>_field_guide.md` are worth preserving long-term.

## Prerequisites
- A Better BibTeX (BBT) JSON export of a Zotero collection, placed at `sources/<source_name>/raw/<export>.json`, with attached PDFs in a `files/` folder next to it (this is how Zotero writes BBT exports with attachments — the scripts resolve attachment paths relative to the export JSON's own folder).
- Python 3 with `PyMuPDF` installed for PDF text extraction: `pip install pymupdf`.
- Python 3 with `scikit-learn` installed if you want to use the topic-modeling assist script in step 2: `pip install scikit-learn`.

## Adding a new source (quick start)

```bash
NAME=my_new_source   # e.g. "nyt_cooking", "krebs_security"

mkdir -p sources/$NAME/raw sources/$NAME/work
# Copy/export your Zotero BBT JSON + files/ folder into sources/$NAME/raw/

# Write sources/$NAME/categories.json (copy sources/lifehacker/categories.json as a starting
# template and adjust the category names/keywords to fit this source's subject matter)

python3 scripts/field_guide/extract_excerpts.py \
  --input sources/$NAME/raw/<export>.json \
  --output sources/$NAME/work/excerpts.json

python3 scripts/field_guide/categorize.py \
  --input sources/$NAME/work/excerpts.json \
  --config sources/$NAME/categories.json \
  --outdir sources/$NAME/work/categories

python3 scripts/field_guide/chunk.py \
  --indir sources/$NAME/work/categories \
  --outdir sources/$NAME/work/chunks \
  --size 20

# --- LLM synthesis happens here: one .md per chunk, saved to sources/$NAME/work/sections/ ---

python3 scripts/field_guide/merge_and_fix_footnotes.py \
  --sections-dir sources/$NAME/work/sections \
  --output sources/$NAME/work/merged_draft.md

python3 scripts/field_guide/validate.py sources/$NAME/work/merged_draft.md

# --- accuracy review + archiving happens here, editing a copy as sources/$NAME/${NAME}_field_guide.md ---

python3 scripts/field_guide/validate.py sources/$NAME/${NAME}_field_guide.md
```

The rest of this document explains each step in detail.

## Workflow Steps

### 1. Extract Metadata and Excerpts
Parse the Zotero JSON export to extract titles, URLs, tags, and a short excerpt from each attached PDF, so later steps don't have to ingest full documents.

**Script:** `scripts/field_guide/extract_excerpts.py`

```bash
python3 scripts/field_guide/extract_excerpts.py \
  --input sources/<name>/raw/<export>.json \
  --output sources/<name>/work/excerpts.json \
  --pdf-chars 800
```

For each top-level item it records `key`, `title`, `url`, `date`, `tags`, `creators`, and an `excerpt` (first N characters of the first PDF attachment's text, falling back to the item's `abstractNote` if no PDF is attached).

### 2. Thematic Categorization
Group the flattened items into broad themes using keyword matching against title + tags.

**Script:** `scripts/field_guide/categorize.py`

```bash
python3 scripts/field_guide/categorize.py \
  --input sources/<name>/work/excerpts.json \
  --config sources/<name>/categories.json \
  --outdir sources/<name>/work/categories
```

`categories.json` is a per-source config, e.g.:

```json
{
  "Finance_Money": ["money", "tax", "budget", "credit", "loan"],
  "Health_Diet_Fitness": ["health", "diet", "fitness", "sleep", "workout"]
}
```

Items are assigned to the first category whose keyword matches (config order matters — put more specific categories first). Anything unmatched lands in a catch-all bucket (default `Miscellaneous`, override with `--catchall`). `sources/lifehacker/categories.json` is a working example; re-tune the keyword lists for each new source's subject matter, and check the catch-all bucket's size afterward — if it's large, add more categories or keywords rather than letting one oversized "misc" bucket carry most of the source.

**Before writing `categories.json` for a new source**, run the topic-modeling assist script to see what's actually in the corpus instead of guessing keywords blind:

```bash
python3 scripts/field_guide/suggest_topics.py \
  --input sources/<name>/work/excerpts.json \
  --topics 12 \
  --output sources/<name>/work/topic_report.md
```

This is a read-only report (top terms + example item titles per discovered topic) — it does not write `categories.json` for you. Read the topics, then write your keyword lists informed by what's actually there. Keywords match as whole words/phrases (not substrings), so list the inflected forms you want to catch, e.g. `["invest", "investing", "investment"]` rather than relying on `"invest"` to substring-match `"investing"`.

### 3. Chunking for 100% Citation Coverage
LLMs tend to omit items when summarizing large lists. To guarantee every source is cited, each category is split into chunks of 15-20 items.

**Script:** `scripts/field_guide/chunk.py`

```bash
python3 scripts/field_guide/chunk.py \
  --indir sources/<name>/work/categories \
  --outdir sources/<name>/work/chunks \
  --size 20
```

Produces `Finance_Money_part1.json`, `Finance_Money_part2.json`, etc.

### 4. LLM Synthesis (Subagent Generation)
Pass each chunk to an LLM (or a swarm of subagents, one per chunk) with a strict prompt, and save the output as one Markdown file per chunk under `sources/<name>/work/sections/`.

**Prompt Template:**
> You are a precise technical writer creating a wiki-style field guide. Read the provided JSON file and synthesize the items into narrative paragraphs.
> **CRITICAL:** You MUST include and cite EVERY SINGLE ITEM present in the JSON. Group related items into flowing narrative paragraphs under subheadings, and start the section with its own top-level heading (e.g. `## Finance & Money`). Cite every item using inline markdown footnotes (e.g., `[^1]`), and list the footnote definitions at the bottom of your output (e.g., `[^1]: [Article Title](URL)`).

Each chunk's output will independently restart its footnotes at `[^1]` — that's expected and fixed in the next step. Give the section its own heading in this step (see `sources/lifehacker/work/sections/section_finance.md` for the expected shape), since the merge script concatenates files as-is without inserting headings itself.

If a category produced more than one chunk (e.g. `Finance_Money_part1.json` and `_part2.json`), you can either synthesize each part into its own section file and list both, in order, when merging, or ask the LLM to merge multiple chunks of the same category into one section file with continuous local footnote numbering before moving to step 5 — either works, since the merge step renumbers per input file regardless.

### 5. Concatenation and Footnote Standardization
Concatenate the section files in your desired final order and renumber all footnotes globally in one pass.

**Script:** `scripts/field_guide/merge_and_fix_footnotes.py`

```bash
# Explicit order (recommended — controls the final section order):
python3 scripts/field_guide/merge_and_fix_footnotes.py \
  --output sources/<name>/work/merged_draft.md \
  sources/<name>/work/sections/section_finance.md \
  sources/<name>/work/sections/section_health.md \
  ...

# Or, alphabetical order straight from a directory:
python3 scripts/field_guide/merge_and_fix_footnotes.py \
  --sections-dir sources/<name>/work/sections \
  --output sources/<name>/work/merged_draft.md
```

It strips each file's `[^N]:` definitions, renumbers them (and their inline references) into one global sequence in the order files are processed, and appends a single `### References` block at the end. Optionally pass `--intro <file.md>` to prepend a title/editorial-note block before the first section.

### 6. Accuracy and Timeliness Review
Copy `merged_draft.md` to `sources/<name>/<name>_field_guide.md` and review it for claims that may be inaccurate, overstated, or time-sensitive — especially for articles about apps, web services, browser settings, operating systems, laws, government rules, prices, travel, health, security incidents, and one-time settlements or promotions.

**Review checklist:**
- Confirm every cited item is still represented once in the body or Archive.
- Search the draft for overconfident language such as "always," "never," "guaranteed," "current," "now," "will," "must," and "best."
- Compare suspicious claims against the extracted local source excerpts first (`work/excerpts.json` / `work/categories/*.json`).
- Use current web sources when the claim could have changed since publication. Prefer official sources for policies, laws, app/service status, browser/platform behavior, and security features.
- Soften claims that remain useful but are not timeless. For example, replace "this ensures..." with "this can help..." or "the cited article recommends..."
- Remove or reframe advice that depends on old UI, old settings, discontinued tools, expired events, or obsolete legal/policy conditions.

### 7. Archive Outdated or Historical Items
Do not delete outdated items outright. Move them into a dedicated `# Archive: outdated or historical tips` section immediately before `### References`, keeping their original citations intact. Explain why each item was moved so future readers understand whether the issue is a discontinued product, changed platform behavior, expired settlement, superseded security event, or time-sensitive pricing/legal advice.

**Archive candidates include:**
- Discontinued apps, sites, browser extensions, or web services.
- Deprecated browser/platform settings or OS-specific UI instructions.
- Security tools tied to a one-time vulnerability or old incident.
- Legal, travel, tax, benefits, or compensation advice based on old rules.
- Retail, pricing, settlement, promotion, or event-based advice with an expired window.

**Archive entry style:**
- Group items under short subheadings such as `Discontinued Apps, Services, and Programs`, `Superseded Security and Platform Advice`, `Superseded Operating-System and Browser Tweaks`, and `Time-Sensitive Travel and Pricing Advice`.
- Preserve the original footnote citation on each archived item.
- State the reason plainly: "shut down," "deprecated," "replaced by modern feature," "rules changed or must be verified," or "time-limited settlement."

### 8. Final Validation
Run a mechanical citation check after every major edit, especially after archiving.

**Script:** `scripts/field_guide/validate.py`

```bash
python3 scripts/field_guide/validate.py sources/<name>/<name>_field_guide.md
```

Checks:
- Number of inline citations matches the number of reference definitions (no missing, no unused, no duplicates).
- Exactly one `### References` (or other `#`-level "References") heading.
- No leftover chunk artifacts (`Part 1`, `part2`, etc.) outside of URLs.

## Output
You will be left with `sources/<name>/<name>_field_guide.md`: a single Markdown file with narrative paragraphs, properly sequenced inline footnotes, an Archive for outdated or historical advice, and a master reference list at the bottom — ready to drop into an Obsidian or Logseq vault without silently presenting obsolete tips as current recommendations.

`sources/lifehacker/lifehacker_field_guide.md` is the reference example this whole workflow was built from.
