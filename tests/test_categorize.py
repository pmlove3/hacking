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


def test_keyword_with_regex_metacharacters_matches_literally():
    # Regex metacharacters inside a keyword must be treated as literal text
    # (via re.escape), not interpreted as regex syntax. Keywords here have
    # word characters at both edges so the \b boundary check itself isn't
    # what's under test -- only the escaping is.
    # Unescaped, "a+b" means "one or more a, then b" and would match "aaab".
    assert matches_category("the code says aaab here", ["a+b"]) is False
    assert matches_category("the code says a+b here", ["a+b"]) is True
    # Unescaped, "c.io" means "c, any char, io" and would match "cXio".
    assert matches_category("visit cXio today", ["c.io"]) is False
    assert matches_category("visit c.io today", ["c.io"]) is True
