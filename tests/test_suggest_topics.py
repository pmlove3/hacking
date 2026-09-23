from suggest_topics import build_documents
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


def test_build_documents_combines_title_and_excerpt():
    items = [{"title": "Ask Your Loan Servicer", "excerpt": "Extra payments go to principal."}]
    assert build_documents(items) == ["Ask Your Loan Servicer Extra payments go to principal."]


def test_build_documents_handles_missing_excerpt():
    items = [{"title": "Just A Title"}]
    assert build_documents(items) == ["Just A Title"]


def test_build_documents_handles_missing_title():
    items = [{"excerpt": "Only an excerpt here."}]
    assert build_documents(items) == ["Only an excerpt here."]


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
