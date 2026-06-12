"""DL002: Detect future tense in documentation."""

import re
from typing import List

from docs_linter.rules.base import Rule, Violation, Severity

# "will" + verb (but not "will" as a noun, e.g., "free will")
FUTURE_PATTERN = re.compile(
    r"\b(will|shall)\s+(not\s+)?(be\s+)?(\w+)",
    re.IGNORECASE,
)

# Common false positives where "will" is a noun or name
FALSE_POSITIVES = {"will", "goodwill", "free will"}


class FutureTenseRule(Rule):
    """Detect future tense usage in technical documentation."""

    id = "DL002"
    name = "no-future-tense"
    description = "Avoid future tense. Use simple present tense in documentation."
    severity = Severity.WARNING

    def check(self, text: str, line_num: int, file_path: str) -> List[Violation]:
        violations = []

        for match in FUTURE_PATTERN.finditer(text):
            full_match = match.group(0)

            # Skip if "will" is likely a noun (preceded by "free", "good", etc.)
            start = match.start()
            prefix = text[max(0, start - 6):start].strip().lower()
            if prefix.endswith(("free", "good", "strong")):
                continue

            col = start + 1
            verb = match.group(4)

            violations.append(self._make_violation(
                file_path=file_path,
                line_num=line_num,
                column=col,
                message=f'Future tense: "{full_match}"',
                suggestion=f"Use present tense instead.",
                context=text.rstrip(),
            ))

        return violations
