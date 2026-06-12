"""DL004: Detect permissive language patterns."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

# Patterns like "lets you", "allows you to", "enables you to", "helps you"
PERMISSIVE_PATTERNS = [
    (re.compile(r"\b(lets?\s+you)\b", re.IGNORECASE), "Use imperative voice instead"),
    (re.compile(r"\b(allows?\s+you\s+to)\b", re.IGNORECASE), "Use imperative voice instead"),
    (re.compile(r"\b(enables?\s+you\s+to)\b", re.IGNORECASE), "Use imperative voice instead"),
    (re.compile(r"\b(helps?\s+you(\s+to)?)\b", re.IGNORECASE), "Use imperative voice instead"),
    (re.compile(r"\b(gives?\s+you\s+the\s+ability\s+to)\b", re.IGNORECASE), "Use imperative voice instead"),
    (re.compile(r"\b(provides?\s+you\s+with)\b", re.IGNORECASE), "State what the user gets directly"),
    (re.compile(r"\b(makes?\s+it\s+possible\s+to)\b", re.IGNORECASE), "Use imperative voice instead"),
]


class PermissiveLanguageRule(Rule):
    """Detect permissive language that distances the reader from the action."""

    id = "DL004"
    name = "no-permissive-language"
    description = 'Avoid "lets you" / "allows you to" / "enables you to". Use imperative voice.'
    severity = Severity.WARNING

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        for pattern, suggestion in PERMISSIVE_PATTERNS:
            for match in pattern.finditer(text):
                col = match.start() + 1

                violations.append(self._make_violation(
                    file_path=file_path,
                    line_num=line_num,
                    column=col,
                    message=f'Permissive language: "{match.group(1)}"',
                    suggestion=suggestion,
                    context=text.rstrip(),
                ))

        return violations
