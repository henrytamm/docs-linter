"""Tests for DL001: no-passive-voice rule."""

import pytest

from docs_linter.rules.passive_voice import PassiveVoiceRule


@pytest.fixture
def rule():
    return PassiveVoiceRule()


@pytest.mark.parametrize("text", [
    "The file is created by the system.",
    "The token was generated automatically.",
    "The results are displayed on the dashboard.",
    "Data is processed every hour.",
    "The request was rejected by the server.",
    "The configuration is stored in a YAML file.",
    "Events are captured in real time.",
])
def test_flags_passive_voice(rule, text):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) > 0
    assert violations[0].rule_id == "DL001"


@pytest.mark.parametrize("text", [
    "Create the file.",
    "The system generates a token.",
    "Display the results on the dashboard.",
    "This is a configuration file.",
    "The API is fast and reliable.",
    "There is a limit of 100 requests.",
    "Run the command to start the server.",
])
def test_passes_active_voice(rule, text):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) == 0
