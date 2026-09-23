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
