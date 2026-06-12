"""DL010: Detect placeholder and draft text."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

PLACEHOLDER_PATTERNS = [
    (re.compile(r"\bTODO\b"), "TODO marker"),
    (re.compile(r"\bFIXME\b"), "FIXME marker"),
    (re.compile(r"\bTBD\b"), "TBD placeholder"),
    (re.compile(r"\bXXX\b"), "XXX marker"),
    (re.compile(r"\bHACK\b"), "HACK marker"),
    (re.compile(r"\bLorem\s+ipsum\b", re.IGNORECASE), "Lorem ipsum placeholder"),
    (re.compile(r"\b(?:foo|bar|baz)\b", re.IGNORECASE), "Example placeholder name"),
    (re.compile(r"\[TBD\]"), "TBD bracket placeholder"),
    (re.compile(r"\[TODO\]"), "TODO bracket placeholder"),
    (re.compile(r"\[INSERT\b", re.IGNORECASE), "INSERT placeholder"),
]


class PlaceholderTextRule(Rule):
    """Detect placeholder text that shouldn't appear in published docs."""

    id = "DL010"
    name = "no-placeholder-text"
    description = "Remove placeholder text (TODO, TBD, Lorem ipsum, etc.) before publishing."
    severity = Severity.ERROR

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        for pattern, label in PLACEHOLDER_PATTERNS:
            for match in pattern.finditer(text):
                col = match.start() + 1

                violations.append(self._make_violation(
                    file_path=file_path,
                    line_num=line_num,
                    column=col,
                    message=f'Placeholder text: "{match.group(0)}" ({label})',
                    suggestion="Replace with final content or remove before publishing.",
                    context=text.rstrip(),
                ))

        return violations
