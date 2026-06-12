"""DL012: Detect non-descriptive link text."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

# Vague link text patterns
CLICK_HERE_PATTERNS = [
    (re.compile(r"\b(click\s+here)\b", re.IGNORECASE), "Use descriptive link text"),
    (re.compile(r"\b(here)\b(?=\s*[\]\)])", re.IGNORECASE), "Use descriptive link text"),
    (re.compile(r"\[(this\s+link)\]", re.IGNORECASE), "Describe where the link goes"),
    (re.compile(r"\[(this\s+page)\]", re.IGNORECASE), "Name the page"),
    (re.compile(r"\[(this\s+article)\]", re.IGNORECASE), "Name the article"),
    (re.compile(r"\[(read\s+more)\]", re.IGNORECASE), "Describe what the reader will learn"),
    (re.compile(r"\[(learn\s+more)\]", re.IGNORECASE), "Describe what the reader will learn"),
]


class ClickHereRule(Rule):
    """Detect non-descriptive link text like 'click here' or 'this link'."""

    id = "DL012"
    name = "no-click-here"
    description = 'Avoid "click here" and vague link text. Use descriptive text that makes sense out of context.'
    severity = Severity.WARNING

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        for pattern, suggestion in CLICK_HERE_PATTERNS:
            for match in pattern.finditer(text):
                col = match.start() + 1

                violations.append(self._make_violation(
                    file_path=file_path,
                    line_num=line_num,
                    column=col,
                    message=f'Non-descriptive link text: "{match.group(1)}"',
                    suggestion=suggestion,
                    context=text.rstrip(),
                ))

        return violations
