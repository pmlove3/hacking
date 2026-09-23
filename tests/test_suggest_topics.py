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
