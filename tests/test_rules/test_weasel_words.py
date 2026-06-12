"""Tests for DL003: no-weasel-words rule."""

import pytest

from docs_linter.rules.weasel_words import WeaselWordsRule


@pytest.fixture
def rule():
    return WeaselWordsRule()


@pytest.mark.parametrize("text,expected_word", [
    ("This might cause issues.", "might"),
    ("You should review the docs.", "should"),
    ("It could fail silently.", "could"),
    ("This is basically a wrapper.", "basically"),
    ("Simply run the command.", "simply"),
    ("This is obviously the right approach.", "obviously"),
])
def test_flags_weasel_words(rule, text, expected_word):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) > 0
    assert expected_word in violations[0].message.lower()


@pytest.mark.parametrize("text", [
    "This can cause issues.",
    "Review the docs before proceeding.",
    "Run the command to start.",
    "The API returns a JSON response.",
])
def test_passes_direct_language(rule, text):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) == 0
