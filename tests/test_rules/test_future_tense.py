"""Tests for DL002: no-future-tense rule."""

import pytest

from docs_linter.rules.future_tense import FutureTenseRule


@pytest.fixture
def rule():
    return FutureTenseRule()


@pytest.mark.parametrize("text", [
    "The system will restart after the update.",
    "This will display the results.",
    "The API will return a JSON response.",
    "Changes will be applied automatically.",
    "The page will not load without credentials.",
])
def test_flags_future_tense(rule, text):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) > 0
    assert violations[0].rule_id == "DL002"


@pytest.mark.parametrize("text", [
    "The system restarts after the update.",
    "This displays the results.",
    "Use free will to decide.",
    "The goodwill of the team matters.",
])
def test_passes_present_tense(rule, text):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) == 0
