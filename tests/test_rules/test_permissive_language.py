"""Tests for DL004: no-permissive-language rule."""

import pytest

from docs_linter.rules.permissive_language import PermissiveLanguageRule


@pytest.fixture
def rule():
    return PermissiveLanguageRule()


@pytest.mark.parametrize("text", [
    "This feature lets you configure webhooks.",
    "The API allows you to query data.",
    "This enables you to build custom integrations.",
    "The SDK helps you capture engagement data.",
    "This gives you the ability to export reports.",
    "The tool provides you with real-time metrics.",
    "This makes it possible to track events.",
])
def test_flags_permissive(rule, text):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) > 0
    assert violations[0].rule_id == "DL004"


@pytest.mark.parametrize("text", [
    "Configure webhooks from the Settings page.",
    "Query data using the REST API.",
    "Build custom integrations with the SDK.",
    "Track events in real time.",
    "Export reports as CSV files.",
])
def test_passes_imperative(rule, text):
    violations = rule.check(text, line_num=1, file_path="test.md")
    assert len(violations) == 0
