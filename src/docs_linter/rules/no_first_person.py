"""DL011: Detect first person pronouns in technical documentation."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

# First person pronouns (skip "us" as it has too many false positives in words)
FIRST_PERSON_PATTERN = re.compile(
    r"\b(I|we|our|my|ourselves|myself)\b",
    re.IGNORECASE,
)

# But don't flag "I" in code-like contexts or when it's clearly an acronym
# Don't flag at the start of a quote
SKIP_CONTEXTS = re.compile(r'["`]')


class NoFirstPersonRule(Rule):
    """Detect first person pronouns in technical documentation."""

    id = "DL011"
    name = "no-first-person"
    description = 'Avoid first person (I, we, our). Use second person (you) or imperative voice.'
    severity = Severity.WARNING

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        for match in FIRST_PERSON_PATTERN.finditer(text):
            word = match.group(1)
            col = match.start() + 1

            # Skip "I" if it looks like a variable or is inside quotes
            if word == "I":
                # Check if surrounded by code-like context
                before = text[max(0, match.start() - 1):match.start()]
                after = text[match.end():match.end() + 1]
                if before in ("`", '"', "'", "/", ".") or after in ("`", '"', "'", "/", "."):
                    continue

            violations.append(self._make_violation(
                file_path=file_path,
                line_num=line_num,
                column=col,
                message=f'First person: "{word}"',
                suggestion="Use second person (you/your) or imperative voice.",
                context=text.rstrip(),
            ))

        return violations
