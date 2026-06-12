"""Rule registry and discovery."""

from docs_linter.rules.base import Rule, Violation, Severity
from docs_linter.rules.passive_voice import PassiveVoiceRule
from docs_linter.rules.future_tense import FutureTenseRule
from docs_linter.rules.weasel_words import WeaselWordsRule
from docs_linter.rules.permissive_language import PermissiveLanguageRule
from docs_linter.rules.doubled_words import DoubledWordsRule
from docs_linter.rules.sentence_length import SentenceLengthRule
from docs_linter.rules.heading_style import HeadingStyleRule
from docs_linter.rules.placeholder_text import PlaceholderTextRule
from docs_linter.rules.no_first_person import NoFirstPersonRule
from docs_linter.rules.click_here import ClickHereRule

ALL_RULES = [
    PassiveVoiceRule,
    FutureTenseRule,
    WeaselWordsRule,
    PermissiveLanguageRule,
    DoubledWordsRule,
    SentenceLengthRule,
    HeadingStyleRule,
    PlaceholderTextRule,
    NoFirstPersonRule,
    ClickHereRule,
]


def get_all_rules():
    """Return instances of all available rules."""
    return [rule_cls() for rule_cls in ALL_RULES]


def get_rule_by_id(rule_id):
    """Look up a rule class by its ID."""
    for rule_cls in ALL_RULES:
        if rule_cls.id == rule_id:
            return rule_cls
    return None

__all__ = [
    "Rule",
    "Violation",
    "Severity",
    "ALL_RULES",
    "get_all_rules",
    "get_rule_by_id",
]
