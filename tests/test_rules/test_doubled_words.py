"""Tests for DL005: no-doubled-words rule."""

import pytest

from docs_linter.rules.doubled_words import DoubledWordsRule


@pytest.fixture
def rule():
    return DoubledWordsRule()


@pytest.mark.parametrize("text", [
    "Click the the button to continue.",
    "This is is a problem.",
    "Enter the value in in the field.",
    "The system will will restart.",
])
def test_flags_doubled_words(rule, text):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) > 0
    assert violations[0].rule_id == "DL005"


@pytest.mark.parametrize("text", [
    "Click the button to continue.",
    "This is a normal sentence.",
    "I had had enough of the errors.",  # "had had" is allowed
    "No no, that is wrong.",  # "no no" is allowed
])
def test_passes_clean_text(rule, text):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) == 0
