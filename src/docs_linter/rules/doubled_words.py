"""DL005: Detect doubled/repeated words."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

# Match any word repeated immediately after itself
DOUBLED_PATTERN = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)

# Words that are legitimately repeated
ALLOWED_DOUBLES = {"had", "that", "no"}


class DoubledWordsRule(Rule):
    """Detect accidentally doubled words (e.g., 'the the')."""

    id = "DL005"
    name = "no-doubled-words"
    description = "Remove accidentally repeated words."
    severity = Severity.ERROR

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        for match in DOUBLED_PATTERN.finditer(text):
            word = match.group(1).lower()

            # Skip intentional doubles
            if word in ALLOWED_DOUBLES:
                continue

            col = match.start() + 1

            violations.append(self._make_violation(
                file_path=file_path,
                line_num=line_num,
                column=col,
                message=f'Doubled word: "{match.group(0)}"',
                suggestion=f"Remove the duplicate '{match.group(1)}'",
                context=text.rstrip(),
            ))

        return violations
